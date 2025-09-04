# dwt_algorithm.py - FIXED VERSION with proper QIM and detection
import numpy as np
import cv2
import time
import pywt
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import os


class DWTSteganography:
    def __init__(self):
        self.wavelet = 'haar'
        self.mode = 'periodization'
        self.embedding_strength = 2.0  # Δ step for QIM
        self.embed_channel = 0         # Blue channel

    # ---------- Helpers for padding ----------

    def _pad_to_multiple(self, arr, base=4):
        """Pad array reflectively so both dims are multiples of `base`."""
        h, w = arr.shape
        pad_h = (base - (h % base)) % base
        pad_w = (base - (w % base)) % base
        if pad_h == 0 and pad_w == 0:
            return arr, (0, 0, 0, 0)  # no padding
        padded = np.pad(arr,
                        ((0, pad_h), (0, pad_w)),
                        mode="reflect")
        return padded, (0, pad_h, 0, pad_w)

    def _crop_to_original(self, arr, pad_info):
        """Crop array back to original size using pad_info."""
        top, bottom, left, right = pad_info
        h, w = arr.shape
        return arr[0:h - bottom, 0:w - right] if (bottom or right) else arr

    # ---------- Text <-> binary ----------

    def text_to_binary(self, text: str) -> str:
        return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

    def binary_to_text(self, binary: str) -> str:
        if len(binary) % 8 != 0:
            binary = binary + '0' * (8 - (len(binary) % 8))
        try:
            b = bytearray(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))
            return b.decode('utf-8', errors='ignore').rstrip('\x00')
        except:
            return "Extraction Error: Invalid binary data"

    # ---------- QIM embedding/extraction ----------

    def _qim_embed(self, x: float, bit: str, Δ: float) -> float:
        """Quantization Index Modulation embedding"""
        if abs(x) < 0.1:  # Avoid very small coefficients
            x = 1.0 if x >= 0 else -1.0
        
        d = 0.0 if bit == '0' else Δ
        quantized = (2 * Δ) * np.round((x - d) / (2 * Δ)) + d
        return quantized

    def _qim_extract_bit(self, x: float, Δ: float) -> str:
        """Extract bit using QIM"""
        r0 = np.mod(x, 2 * Δ)
        r1 = np.mod(x - Δ, 2 * Δ)
        d0 = np.minimum(r0, 2 * Δ - r0)
        d1 = np.minimum(r1, 2 * Δ - r1)
        return '1' if d1 < d0 else '0'

    # ---------- Metrics ----------

    def calculate_real_metrics(self, original, stego):
        """Calculate quality metrics"""
        h = min(original.shape[0], stego.shape[0])
        w = min(original.shape[1], stego.shape[1])
        original = original[:h, :w]
        stego = stego[:h, :w]

        orig_f = original.astype(np.float64)
        steg_f = stego.astype(np.float64)

        mse = np.mean((orig_f - steg_f) ** 2)
        psnr = 100.0 if mse == 0 else 20 * np.log10(255.0 / np.sqrt(mse))
        signal_power = np.mean(orig_f ** 2)
        snr = 100.0 if signal_power == 0 or mse == 0 else 10 * np.log10(signal_power / mse)

        if len(original.shape) == 3:
            ssim_val = np.mean([ssim(original[:, :, i], stego[:, :, i], data_range=255) for i in range(3)])
        else:
            ssim_val = ssim(original, stego, data_range=255)

        return {'mse': float(mse), 'psnr': float(psnr), 'snr': float(snr), 'ssim': float(ssim_val)}

    # ---------- Embed ----------

    def embed_text(self, image_path: str, secret_text: str):
        """Embed text using DWT with comprehensive metrics"""
        start_time = time.time()
        
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")
        original_image = image.copy().astype(np.uint8)
        stego_image = image.astype(np.float64)

        # Pad channel
        channel = stego_image[:, :, self.embed_channel]
        channel_padded, pad_info = self._pad_to_multiple(channel, 4)

        # Prepare message with length header
        text_bytes = secret_text.encode('utf-8')
        text_length = len(text_bytes)
        header_bits = format(text_length, '032b')
        payload_bits = ''.join(format(b, '08b') for b in text_bytes)
        full_message = header_bits + payload_bits

        # DWT decomposition
        coeffs2 = pywt.wavedec2(channel_padded, self.wavelet, level=2, mode=self.mode)
        cA2 = coeffs2[0]
        cH2, cV2, cD2 = coeffs2[1]
        cH1, cV1, cD1 = coeffs2[2]

        # Embed in mid-frequency coefficients (cH2)
        flat = cH2.flatten()
        Δ = float(self.embedding_strength)

        if len(full_message) > flat.size:
            raise ValueError(f"Message too long! Need {len(full_message)} coefficients, but only {flat.size} available")

        # Embedding process
        for i, bit in enumerate(full_message):
            flat[i] = self._qim_embed(flat[i], bit, Δ)

        # Reconstruct
        cH2_mod = flat.reshape(cH2.shape)
        coeffs2_mod = [cA2, (cH2_mod, cV2, cD2), (cH1, cV1, cD1)]
        stego_channel = pywt.waverec2(coeffs2_mod, self.wavelet, mode=self.mode)

        # Crop to original size
        stego_channel = self._crop_to_original(stego_channel, pad_info)
        stego_image[:, :, self.embed_channel] = stego_channel
        stego_image = np.clip(stego_image, 0, 255).astype(np.uint8)

        embedding_time = time.time() - start_time

        # Calculate metrics
        metrics = self.calculate_real_metrics(original_image, stego_image)
        
        # Add embedding-specific metrics
        metrics.update({
            'embedding_time': embedding_time,
            'text_length': text_length,
            'bits_embedded': len(full_message),
            'capacity': flat.size,
            'capacity_usage': (len(full_message) / flat.size) * 100,
            'wavelet': self.wavelet,
            'embedding_channel': 'Blue',
            'embedding_strength': self.embedding_strength
        })

        return stego_image, metrics

    # ---------- Extract ----------

    def extract_text(self, stego_image_path: str):
        """Extract text from stego image with timing"""
        start_time = time.time()
        
        try:
            stego_image = cv2.imread(stego_image_path)
            if stego_image is None:
                return "Error: Could not read stego image", 0.0

            channel = stego_image[:, :, self.embed_channel].astype(np.float64)
            channel_padded, pad_info = self._pad_to_multiple(channel, 4)

            # DWT decomposition
            coeffs2 = pywt.wavedec2(channel_padded, self.wavelet, level=2, mode=self.mode)
            cH2 = coeffs2[1][0]  # Mid-frequency coefficients
            flat = cH2.flatten()
            Δ = float(self.embedding_strength)

            # Extract header (32 bits for text length)
            header_bits = ''.join(self._qim_extract_bit(x, Δ) for x in flat[:32])
            try:
                text_length = int(header_bits, 2)
            except ValueError:
                return "Error: Invalid header data", time.time() - start_time

            if text_length <= 0 or text_length > 10000:  # Reasonable limits
                return "Error: Invalid text length in header", time.time() - start_time

            required_bits = text_length * 8
            if 32 + required_bits > len(flat):
                return "Error: Not enough coefficients for extraction", time.time() - start_time

            # Extract payload
            payload = flat[32:32 + required_bits]
            message_bits = ''.join(self._qim_extract_bit(x, Δ) for x in payload)

            extracted_text = self.binary_to_text(message_bits)
            extraction_time = time.time() - start_time

            return extracted_text, extraction_time

        except Exception as e:
            return f"Error: {str(e)}", time.time() - start_time

    # ---------- Detection and Analysis ----------

    def analyze_image(self, image_path: str):
        """Analyze image for steganography with DWT-specific detection"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {'is_suspicious': False, 'confidence': 0, 'details': [], 'analysis_method': 'DWT'}

            # DWT coefficient analysis
            channel = image[:, :, self.embed_channel].astype(np.float64)
            channel_padded, _ = self._pad_to_multiple(channel, 4)

            coeffs2 = pywt.wavedec2(channel_padded, self.wavelet, level=2, mode=self.mode)
            cH2 = coeffs2[1][0].flatten()

            # Statistical analysis
            details = []
            suspicion_score = 0

            # Check for quantization artifacts
            Δ = self.embedding_strength
            quantization_residue = []
            for coeff in cH2[:100]:  # Sample first 100 coefficients
                r0 = np.mod(coeff, 2 * Δ)
                r1 = np.mod(coeff - Δ, 2 * Δ)
                d0 = np.minimum(r0, 2 * Δ - r0)
                d1 = np.minimum(r1, 2 * Δ - r1)
                quantization_residue.append(min(d0, d1))

            avg_residue = np.mean(quantization_residue)
            if avg_residue < 0.5:
                suspicion_score += 30
                details.append(f"Low quantization residue detected: {avg_residue:.3f}")

            # Check coefficient distribution
            coeff_std = np.std(cH2)
            if coeff_std > 10 and coeff_std < 50:
                suspicion_score += 25
                details.append(f"Suspicious coefficient std deviation: {coeff_std:.2f}")

            # Try extraction to verify
            extracted_text, _ = self.extract_text(image_path)
            if extracted_text and not extracted_text.startswith("Error") and len(extracted_text.strip()) > 0:
                suspicion_score += 45
                details.append(f"Valid text extracted: '{extracted_text[:50]}...'")
                return {
                    'is_suspicious': True,
                    'confidence': min(100, suspicion_score),
                    'details': details,
                    'analysis_method': 'DWT Coefficient Analysis',
                    'extracted_text': extracted_text
                }

            is_suspicious = suspicion_score > 40
            confidence = min(suspicion_score, 95) if is_suspicious else max(5, 100 - suspicion_score)

            return {
                'is_suspicious': is_suspicious,
                'confidence': confidence,
                'details': details,
                'analysis_method': 'DWT Coefficient Analysis'
            }

        except Exception as e:
            return {'is_suspicious': False, 'confidence': 0, 'details': [f"Analysis error: {e}"], 'analysis_method': 'DWT'}

    def save_stego_image(self, stego_array, output_path):
        """Save stego image"""
        try:
            success = cv2.imwrite(output_path, stego_array)
            return success
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    def detect_steganography(self, image_path: str):
        """Legacy compatibility method"""
        result = self.analyze_image(image_path)
        return result['is_suspicious'], result['confidence'], result['details']


# -------- Test --------
if __name__ == "__main__":
    dwt = DWTSteganography()
    
    # Create test image if it doesn't exist
    test_image = "test_input.png"
    if not os.path.exists(test_image):
        test_img = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
        cv2.imwrite(test_image, test_img)
        print(f"Created test image: {test_image}")
    
    try:
        # Test embedding
        stego, metrics = dwt.embed_text(test_image, "Hello DWT Steganography!")
        
        # Save stego image
        output_path = "test_stego.png"
        if dwt.save_stego_image(stego, output_path):
            print(f"Embedding successful! Saved to: {output_path}")
            print(f"PSNR: {metrics['psnr']:.2f} dB")
            print(f"SSIM: {metrics['ssim']:.4f}")
            print(f"Embedding time: {metrics['embedding_time']:.3f}s")
            
            # Test extraction
            extracted, ext_time = dwt.extract_text(output_path)
            print(f"Extracted text: '{extracted}'")
            print(f"Extraction time: {ext_time:.3f}s")
            
            # Test detection
            analysis = dwt.analyze_image(output_path)
            print(f"Detection: {'POSITIVE' if analysis['is_suspicious'] else 'NEGATIVE'}")
            print(f"Confidence: {analysis['confidence']:.0f}%")
        else:
            print("Failed to save stego image")
            
    except Exception as e:
        print(f"Test failed: {e}")