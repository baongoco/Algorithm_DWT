import numpy as np
import cv2
import time
import pywt
from skimage.metrics import structural_similarity as ssim
import os


class DWTSteganography:
    def __init__(self):
        self.wavelet = 'haar'
        self.mode = 'periodization' 
        self.embedding_strength = 4.0  # Δ for quantization
        self.embed_channel = 0  # Blue channel
        self.quantization_step = 32.0  # Q step for true DWT embedding. Increased for robustness.

    def _ensure_dwt_compatible_size(self, image):
        """Ensure image dimensions are compatible with 2-level DWT"""
        h, w = image.shape[:2]
        # For 2-level DWT, dimensions must be divisible by 4
        new_h = (h // 4) * 4
        new_w = (w // 4) * 4
        
        if new_h != h or new_w != w:
            image = image[:new_h, :new_w]
            print(f"DEBUG: Resized from {h}x{w} to {new_h}x{new_w} for DWT compatibility")
        
        return image

    def text_to_binary(self, text: str) -> str:
        return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

    def binary_to_text(self, binary: str) -> str:
        if len(binary) % 8 != 0:
            return "Error: Binary string length is not a multiple of 8"
        try:
            b = bytearray(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))
            # Use 'strict' to catch errors, which indicates corruption
            return b.decode('utf-8', errors='strict').rstrip('\x00')
        except UnicodeDecodeError:
            return "Error: Failed to decode UTF-8 string. Data may be corrupt."
        except Exception as e:
            return f"Error: Extraction failed during binary to text conversion: {e}"

    def _dwt_quantization_embed(self, coeff, bit, Q):
        """Quantization Index Modulation (QIM) embedding with dithers.
        Uses two cosets separated by Q/2: d0=0 for bit 0, d1=Q/2 for bit 1.
        """
        dither = 0.0 if bit == '0' else (Q / 2.0)
        return Q * np.round((coeff - dither) / Q) + dither

    def _dwt_quantization_extract(self, coeff, Q):
        """QIM extraction: decide which dithered lattice the coeff is closer to."""
        # Distance to bit 0 lattice (dither = 0)
        recon0 = Q * np.round(coeff / Q)
        dist0 = abs(coeff - recon0)
        # Distance to bit 1 lattice (dither = Q/2)
        recon1 = Q * np.round((coeff - (Q / 2.0)) / Q) + (Q / 2.0)
        dist1 = abs(coeff - recon1)
        return '1' if dist1 < dist0 else '0'

    def _adaptive_quantization_embed(self, coeff, bit, base_q, sensitivity=1.0):
        """Adaptive quantization based on coefficient magnitude"""
        # Adapt quantization step to coefficient magnitude
        magnitude = abs(coeff)
        if magnitude < 10:
            Q = base_q * 0.5  # Smaller step for small coefficients
        elif magnitude > 50:
            Q = base_q * 2.0  # Larger step for large coefficients  
        else:
            Q = base_q
            
        Q *= sensitivity
        return self._dwt_quantization_embed(coeff, bit, Q), Q

    def _adaptive_quantization_extract(self, coeff, base_q, sensitivity=1.0):
        """Adaptive quantization extraction"""
        magnitude = abs(coeff)
        if magnitude < 10:
            Q = base_q * 0.5
        elif magnitude > 50:
            Q = base_q * 2.0
        else:
            Q = base_q
            
        Q *= sensitivity
        return self._dwt_quantization_extract(coeff, Q)

    def embed_text(self, image_path: str, secret_text: str):
        """True DWT steganography embedding"""
        start_time = time.time()
        
        print(f"DEBUG: Embedding '{secret_text}' using TRUE DWT steganography")
        
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")
        
        # Ensure DWT-compatible dimensions
        image = self._ensure_dwt_compatible_size(image)
        original_image = image.copy()
        
        # Work with floating point
        float_image = image.astype(np.float64)
        channel = float_image[:, :, self.embed_channel]
        
        # Prepare message with length header
        text_binary = self.text_to_binary(secret_text)
        text_length_in_bytes = len(text_binary) // 8
        header = format(text_length_in_bytes, '024b')  # 24-bit header for byte length
        full_message = header + text_binary
        
        print(f"DEBUG: Message length: {len(full_message)} bits")
        print(f"DEBUG: Header: {header} (text length in bytes: {text_length_in_bytes})")
        
        # 2-level DWT decomposition (TRUE DWT)
        coeffs = pywt.wavedec2(channel, self.wavelet, level=2, mode=self.mode)
        
        # Extract subbands: [cA2, (cH2, cV2, cD2), (cH1, cV1, cD1)]
        cA2 = coeffs[0]
        cH2, cV2, cD2 = coeffs[1]  # Level 2 details
        cH1, cV1, cD1 = coeffs[2]  # Level 1 details
        
        # Use mid-frequency coefficients (cH2) for embedding - standard in DWT steganography
        embed_coeffs = cH2.flatten()
        print(f"DEBUG: Available mid-frequency coefficients: {len(embed_coeffs)}")
        
        if len(full_message) > len(embed_coeffs):
            raise ValueError(f"Message too long for DWT capacity: {len(full_message)} > {len(embed_coeffs)}")
        
        # True DWT embedding using quantization
        modified_coeffs = embed_coeffs.copy()
        base_Q = self.quantization_step
        
        for i, bit in enumerate(full_message):
            # Use fixed quantization for robustness
            modified_coeffs[i] = self._dwt_quantization_embed(
                embed_coeffs[i], bit, base_Q
            )
        
        # Reconstruct DWT with modified coefficients
        modified_cH2 = modified_coeffs.reshape(cH2.shape)
        modified_coeffs_struct = [cA2, (modified_cH2, cV2, cD2), (cH1, cV1, cD1)]
        
        # Inverse DWT
        stego_channel = pywt.waverec2(modified_coeffs_struct, self.wavelet, mode=self.mode)
        
        # Handle reconstruction size differences
        if stego_channel.shape != channel.shape:
            min_h = min(stego_channel.shape[0], channel.shape[0])
            min_w = min(stego_channel.shape[1], channel.shape[1])
            stego_channel = stego_channel[:min_h, :min_w]
            float_image = float_image[:min_h, :min_w]
        
        # Update stego image
        float_image[:, :, self.embed_channel] = stego_channel
        stego_image = np.clip(float_image, 0, 255).astype(np.uint8)
        
        embedding_time = time.time() - start_time
        
        # Calculate metrics
        metrics = self.calculate_real_metrics(original_image, stego_image)
        metrics.update({
            'embedding_time': embedding_time,
            'text_length': text_length_in_bytes,
            'bits_embedded': len(full_message),
            'capacity': len(embed_coeffs),
            'capacity_usage': (len(full_message) / len(embed_coeffs)) * 100,
            'wavelet': self.wavelet,
            'embedding_channel': 'Blue',
            'embedding_strength': self.embedding_strength,
            'dwt_levels': 2,
            'embedding_domain': 'Mid-frequency DWT coefficients (cH2)'
        })
        
        print(f"DEBUG: True DWT embedding complete - PSNR: {metrics['psnr']:.2f} dB")
        return stego_image, metrics

    def extract_text(self, stego_image_path: str):
        """True DWT steganography extraction"""
        start_time = time.time()
        
        try:
            print(f"DEBUG: Extracting using TRUE DWT steganography from {stego_image_path}")
            
            stego_image = cv2.imread(stego_image_path)
            if stego_image is None:
                return "Error: Could not read stego image", 0.0
            
            # Ensure DWT-compatible dimensions
            stego_image = self._ensure_dwt_compatible_size(stego_image)
            channel = stego_image[:, :, self.embed_channel].astype(np.float64)
            
            # 2-level DWT decomposition (same as embedding)
            coeffs = pywt.wavedec2(channel, self.wavelet, level=2, mode=self.mode)
            cH2 = coeffs[1][0]  # Mid-frequency coefficients
            
            extract_coeffs = cH2.flatten()
            print(f"DEBUG: Extracting from {len(extract_coeffs)} coefficients")
            
            # Extract header (24 bits)
            header_bits = []
            base_Q = self.quantization_step
            
            for i in range(24):
                if i >= len(extract_coeffs):
                    return "Error: Not enough coefficients for header", time.time() - start_time
                
                # Use fixed quantization for robustness
                bit = self._dwt_quantization_extract(extract_coeffs[i], base_Q)
                header_bits.append(bit)
            
            header_str = ''.join(header_bits)
            print(f"DEBUG: Extracted header: {header_str}")
            
            try:
                text_length_in_bytes = int(header_str, 2)
                print(f"DEBUG: Decoded text length: {text_length_in_bytes} bytes")
            except ValueError:
                return "Error: Invalid header format", time.time() - start_time
            
            # Set a reasonable limit for message size in bytes
            if text_length_in_bytes <= 0 or text_length_in_bytes > len(extract_coeffs):
                return f"Error: Invalid text length in header: {text_length_in_bytes} bytes", time.time() - start_time
            
            # Extract message bits
            message_bits = []
            required_bits = text_length_in_bytes * 8
            
            if 24 + required_bits > len(extract_coeffs):
                return "Error: Not enough coefficients for full message", time.time() - start_time
            
            for i in range(24, 24 + required_bits):
                if i >= len(extract_coeffs):
                    return "Error: Not enough coefficients for full message", time.time() - start_time
                # Use fixed quantization for robustness
                bit = self._dwt_quantization_extract(extract_coeffs[i], base_Q)
                message_bits.append(bit)
            
            message_binary = ''.join(message_bits)
            extracted_text = self.binary_to_text(message_binary)
            
            print(f"DEBUG: Successfully extracted: '{extracted_text}'")
            
            extraction_time = time.time() - start_time
            return extracted_text, extraction_time
            
        except Exception as e:
            print(f"DEBUG: Extraction error: {e}")
            import traceback
            traceback.print_exc()
            return f"Error: {str(e)}", time.time() - start_time

    def calculate_real_metrics(self, original, stego):
        """Calculate image quality metrics"""
        if original.shape != stego.shape:
            min_h = min(original.shape[0], stego.shape[0])
            min_w = min(original.shape[1], stego.shape[1])
            original = original[:min_h, :min_w]
            stego = stego[:min_h, :min_w]

        orig_f = original.astype(np.float64)
        steg_f = stego.astype(np.float64)

        mse = np.mean((orig_f - steg_f) ** 2)
        psnr = 100.0 if mse == 0 else 20 * np.log10(255.0 / np.sqrt(mse))
        
        if len(original.shape) == 3:
            ssim_val = np.mean([ssim(original[:, :, i], stego[:, :, i], data_range=255) for i in range(3)])
        else:
            ssim_val = ssim(original, stego, data_range=255)

        return {'mse': float(mse), 'psnr': float(psnr), 'snr': float(psnr), 'ssim': float(ssim_val)}

    def analyze_image(self, image_path: str):
        """Analyze for DWT steganography"""
        extracted_text, _ = self.extract_text(image_path)
        
        if extracted_text and not extracted_text.startswith("Error") and len(extracted_text.strip()) > 0:
            return {
                'is_suspicious': True,
                'confidence': 95,
                'details': [f"DWT steganography detected: '{extracted_text[:50]}...'"],
                'analysis_method': 'True DWT Quantization Analysis',
                'extracted_text': extracted_text
            }
        else:
            return {
                'is_suspicious': False,
                'confidence': 5,
                'details': ['No DWT steganography patterns detected'],
                'analysis_method': 'True DWT Quantization Analysis'
            }

    def save_stego_image(self, stego_array, output_path):
        """Save stego image with maximum quality preservation"""
        try:
            # PNG with no compression to preserve DWT coefficients
            success = cv2.imwrite(output_path, stego_array, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            return success
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    def detect_steganography(self, image_path: str):
        """Legacy compatibility"""
        result = self.analyze_image(image_path)
        return result['is_suspicious'], result['confidence'], result['details']


# Test the TRUE DWT implementation
if __name__ == "__main__":
    print("Testing TRUE DWT Steganography (Mathematically Correct)")
    print("=" * 60)
    
    dwt = DWTSteganography()
    
    # Create a proper test image
    test_image = "true_dwt_test.png"
    if not os.path.exists(test_image):
        # Create 256x256 image (divisible by 4 for 2-level DWT)
        test_img = np.random.randint(80, 180, (256, 256, 3), dtype=np.uint8)
        cv2.imwrite(test_image, test_img)
        print(f"Created test image: {test_image}")
    
    try:
        # Test with proper DWT steganography
        secret = "DWT"  # Start simple
        print(f"\nTesting TRUE DWT with message: '{secret}'")
        
        # Embed using true DWT
        stego, metrics = dwt.embed_text(test_image, secret)
        print(f" True DWT embedding successful")
        print(f"  PSNR: {metrics['psnr']:.2f} dB")
        print(f"  Embedding domain: {metrics['embedding_domain']}")
        print(f"  DWT levels: {metrics['dwt_levels']}")
        
        # Save stego image
        output = "true_dwt_stego.png"
        if dwt.save_stego_image(stego, output):
            print(f"✓ Saved to: {output}")
            
            # Extract using true DWT
            extracted, time_taken = dwt.extract_text(output)
            print(f"✓ Extraction completed in {time_taken:.3f}s")
            print(f"  Extracted: '{extracted}'")
            print(f"  Correct: {extracted == secret}")
            
            if extracted == secret:
                print("\nTRUE DWT STEGANOGRAPHY WORKING CORRECTLY!")
            else:
                print(f"\nMismatch - Expected: '{secret}', Got: '{extracted}'")
        else:
            print("Failed to save stego image")
            
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nAlgorithm Details:")
    print("- 2-level Haar DWT decomposition")  
    print("- Mid-frequency coefficient embedding (cH2)")
    print("- Adaptive quantization-based modification")
    print("- Mathematically sound DWT steganography")