import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import pywt
import cv2
import time
import os

class DWTSteganography:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DWT Based Image Steganography")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.input_image_path = None
        self.stego_image_path = None
        self.input_image = None
        self.stego_image = None
        self.embedded_image = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main Title
        title_frame = tk.Frame(self.root, bg='#b53e4a', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="DWT Based Image Steganography (Hiding Secret Text In Image)",
            font=('Arial', 20, 'bold italic'),
            bg='#b53e4a',
            fg='white'
        )
        title_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # EMBEDDING SIDE
        embedding_frame = tk.LabelFrame(
            main_container,
            text="EMBEDDING SIDE",
            font=('Arial', 14, 'bold italic'),
            bg='#87ceeb',
            fg='black',
            relief='ridge',
            borderwidth=3
        )
        embedding_frame.pack(fill='both', expand=True, pady=(0, 5))
        
        # Embedding content
        embed_content = tk.Frame(embedding_frame, bg='#87ceeb')
        embed_content.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left side - Input Image
        left_frame = tk.Frame(embed_content, bg='#87ceeb')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Input image display
        self.input_image_label = tk.Label(
            left_frame,
            text="No Image Selected",
            bg='white',
            width=30,
            height=15,
            relief='sunken'
        )
        self.input_image_label.pack()
        
        tk.Label(left_frame, text="Input Image", font=('Arial', 12, 'italic'), bg='#87ceeb').pack(pady=5)
        
        # Middle - Secret Text
        middle_frame = tk.Frame(embed_content, bg='#87ceeb')
        middle_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        tk.Label(
            middle_frame,
            text="Enter Secret Text To Hide",
            font=('Arial', 12, 'bold'),
            bg='#87ceeb'
        ).pack(pady=(0, 10))
        
        self.secret_text = tk.Text(
            middle_frame,
            width=40,
            height=10,
            font=('Arial', 11),
            wrap='word'
        )
        self.secret_text.pack()
        self.secret_text.insert('1.0', "Hello This is msg")
        
        # Right side - Embedded Image
        right_frame = tk.Frame(embed_content, bg='#87ceeb')
        right_frame.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        # Embedded image display
        self.embedded_image_label = tk.Label(
            right_frame,
            text="Embedded Image Will Appear Here",
            bg='white',
            width=30,
            height=15,
            relief='sunken'
        )
        self.embedded_image_label.pack()
        
        tk.Label(right_frame, text="Embedded Stego Image", font=('Arial', 12, 'italic'), bg='#87ceeb').pack(pady=5)
        
        # Buttons for embedding
        button_frame = tk.Frame(embedding_frame, bg='#87ceeb')
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Browse Input",
            font=('Arial', 12, 'bold'),
            bg='#d8bfd8',
            fg='black',
            width=15,
            height=2,
            command=self.browse_input_image
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Embedding",
            font=('Arial', 12, 'bold'),
            bg='#d8bfd8',
            fg='black',
            width=15,
            height=2,
            command=self.embed_text
        ).pack(side='left', padx=5)
        
        # Parameters for Embedding
        embed_params_frame = tk.Frame(embedding_frame, bg='#ffa500', height=40)
        embed_params_frame.pack(fill='x', padx=10, pady=(5, 10))
        embed_params_frame.pack_propagate(False)
        
        tk.Label(embed_params_frame, text="Parameters", font=('Arial', 12, 'bold italic'), bg='#ffa500').pack(side='left', padx=20)
        
        tk.Label(embed_params_frame, text="Embedding Time:", font=('Arial', 11), bg='#ffa500').pack(side='left', padx=10)
        self.embed_time_label = tk.Label(embed_params_frame, text="", font=('Arial', 11), bg='white', width=15)
        self.embed_time_label.pack(side='left', padx=5)
        
        tk.Label(embed_params_frame, text="SNR:", font=('Arial', 11), bg='#ffa500').pack(side='left', padx=10)
        self.snr_label = tk.Label(embed_params_frame, text="", font=('Arial', 11), bg='white', width=15)
        self.snr_label.pack(side='left', padx=5)
        
        tk.Label(embed_params_frame, text="SSIM:", font=('Arial', 11), bg='#ffa500').pack(side='left', padx=10)
        self.ssim_embed_label = tk.Label(embed_params_frame, text="", font=('Arial', 11), bg='white', width=15)
        self.ssim_embed_label.pack(side='left', padx=5)
        
        # Attribution
        attribution_frame = tk.Frame(self.root, bg='#b53e4a', height=40)
        attribution_frame.pack(fill='x')
        attribution_frame.pack_propagate(False)
        
        tk.Label(
            attribution_frame,
            text="Project By: Prof. Roshan P. Helonde    |    Mobile/WhatsApp: +917276355704",
            font=('Arial', 14, 'bold italic'),
            bg='#b53e4a',
            fg='white'
        ).place(relx=0.5, rely=0.5, anchor='center')
        
        # EXTRACTION SIDE
        extraction_frame = tk.LabelFrame(
            main_container,
            text="EXTRACTION SIDE",
            font=('Arial', 14, 'bold italic'),
            bg='#87ceeb',
            fg='black',
            relief='ridge',
            borderwidth=3
        )
        extraction_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        # Extraction content
        extract_content = tk.Frame(extraction_frame, bg='#87ceeb')
        extract_content.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left side - Stego Image
        extract_left = tk.Frame(extract_content, bg='#87ceeb')
        extract_left.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.stego_image_label = tk.Label(
            extract_left,
            text="No Stego Image Selected",
            bg='white',
            width=30,
            height=15,
            relief='sunken'
        )
        self.stego_image_label.pack()
        
        tk.Label(extract_left, text="Stego Image", font=('Arial', 12, 'italic'), bg='#87ceeb').pack(pady=5)
        
        # Middle - Extracted Text
        extract_middle = tk.Frame(extract_content, bg='#87ceeb')
        extract_middle.pack(side='left', fill='both', expand=True, padx=10)
        
        tk.Label(
            extract_middle,
            text="Extracted Secret Text",
            font=('Arial', 12, 'bold'),
            bg='#87ceeb'
        ).pack(pady=(0, 10))
        
        self.extracted_text = tk.Text(
            extract_middle,
            width=40,
            height=10,
            font=('Arial', 11),
            wrap='word'
        )
        self.extracted_text.pack()
        
        # Right side - Buttons
        extract_right = tk.Frame(extract_content, bg='#87ceeb')
        extract_right.pack(side='right', fill='y', padx=(10, 0))
        
        tk.Button(
            extract_right,
            text="Browse Stego Image",
            font=('Arial', 12, 'bold'),
            bg='#d8bfd8',
            fg='black',
            width=18,
            height=2,
            command=self.browse_stego_image
        ).pack(pady=5)
        
        tk.Button(
            extract_right,
            text="Extraction",
            font=('Arial', 12, 'bold'),
            bg='#d8bfd8',
            fg='black',
            width=18,
            height=2,
            command=self.extract_text
        ).pack(pady=5)
        
        tk.Button(
            extract_right,
            text="Reset",
            font=('Arial', 12, 'bold'),
            bg='#d8bfd8',
            fg='black',
            width=18,
            height=2,
            command=self.reset_all
        ).pack(pady=5)
        
        tk.Button(
            extract_right,
            text="Exit",
            font=('Arial', 12, 'bold'),
            bg='#d8bfd8',
            fg='black',
            width=18,
            height=2,
            command=self.root.quit
        ).pack(pady=5)
        
        # Parameters for Extraction
        extract_params_frame = tk.Frame(extraction_frame, bg='#ffa500', height=40)
        extract_params_frame.pack(fill='x', padx=10, pady=(5, 10))
        extract_params_frame.pack_propagate(False)
        
        tk.Label(extract_params_frame, text="Parameters", font=('Arial', 12, 'bold italic'), bg='#ffa500').pack(side='left', padx=20)
        
        tk.Label(extract_params_frame, text="Extraction Time:", font=('Arial', 11), bg='#ffa500').pack(side='left', padx=10)
        self.extract_time_label = tk.Label(extract_params_frame, text="", font=('Arial', 11), bg='white', width=15)
        self.extract_time_label.pack(side='left', padx=5)
        
        tk.Label(extract_params_frame, text="PSNR:", font=('Arial', 11), bg='#ffa500').pack(side='left', padx=10)
        self.psnr_label = tk.Label(extract_params_frame, text="", font=('Arial', 11), bg='white', width=15)
        self.psnr_label.pack(side='left', padx=5)
        
        tk.Label(extract_params_frame, text="SSIM:", font=('Arial', 11), bg='#ffa500').pack(side='left', padx=10)
        self.ssim_extract_label = tk.Label(extract_params_frame, text="", font=('Arial', 11), bg='white', width=15)
        self.ssim_extract_label.pack(side='left', padx=5)
    
    def browse_input_image(self):
        filename = filedialog.askopenfilename(
            title="Select Input Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if filename:
            self.input_image_path = filename
            self.input_image = cv2.imread(filename)
            self.display_image(filename, self.input_image_label)
            
    def browse_stego_image(self):
        filename = filedialog.askopenfilename(
            title="Select Stego Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if filename:
            self.stego_image_path = filename
            self.stego_image = cv2.imread(filename)
            self.display_image(filename, self.stego_image_label)
            
    def display_image(self, image_path, label):
        try:
            image = Image.open(image_path)
            image = image.resize((250, 250), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label.configure(image=photo, text="")
            label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display image: {str(e)}")
            
    def text_to_binary(self, text):
        binary = ''.join(format(ord(char), '08b') for char in text)
        return binary
    
    def binary_to_text(self, binary):
        text = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text
    
    def embed_text(self):
        if self.input_image is None:
            messagebox.showerror("Error", "Please select an input image first!")
            return
            
        text = self.secret_text.get('1.0', 'end-1c')
        if not text:
            messagebox.showerror("Error", "Please enter text to hide!")
            return
            
        try:
            start_time = time.time()
            
            # Convert text to binary
            binary_text = self.text_to_binary(text)
            binary_text += '1111111111111110'  # End marker
            
            # Convert image to YCrCb
            img_ycrcb = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2YCrCb)
            y_channel = img_ycrcb[:, :, 0].astype(float)
            
            # Apply DWT
            coeffs = pywt.dwt2(y_channel, 'haar')
            LL, (LH, HL, HH) = coeffs
            
            # Embed in LL band
            flat_LL = LL.flatten()
            
            # Embed binary text
            for i, bit in enumerate(binary_text):
                if i < len(flat_LL):
                    flat_LL[i] = int(flat_LL[i]) & 0xFE | int(bit)
                    
            # Reshape and inverse DWT
            LL_embedded = flat_LL.reshape(LL.shape)
            coeffs_embedded = (LL_embedded, (LH, HL, HH))
            y_embedded = pywt.idwt2(coeffs_embedded, 'haar')
            
            # Resize if necessary
            y_embedded = cv2.resize(y_embedded, (img_ycrcb.shape[1], img_ycrcb.shape[0]))
            
            # Replace Y channel
            stego_ycrcb = img_ycrcb.copy()
            stego_ycrcb[:, :, 0] = np.clip(y_embedded, 0, 255).astype(np.uint8)
            
            # Convert back to BGR
            self.embedded_image = cv2.cvtColor(stego_ycrcb, cv2.COLOR_YCrCb2BGR)
            
            # Save stego image
            output_path = "stego_image.png"
            cv2.imwrite(output_path, self.embedded_image)
            
            # Display embedded image
            self.display_image(output_path, self.embedded_image_label)
            
            # Calculate metrics
            end_time = time.time()
            embed_time = end_time - start_time
            
            # Calculate SNR
            signal_power = np.mean(self.input_image.astype(float) ** 2)
            noise = self.input_image.astype(float) - self.embedded_image.astype(float)
            noise_power = np.mean(noise ** 2)
            if noise_power > 0:
                snr = 10 * np.log10(signal_power / noise_power)
            else:
                snr = float('inf')
                
            # Calculate SSIM (simplified version)
            ssim = self.calculate_ssim(self.input_image, self.embedded_image)
            
            # Update labels
            self.embed_time_label.config(text=f"{embed_time:.4f} s")
            self.snr_label.config(text=f"{snr:.2f} dB")
            self.ssim_embed_label.config(text=f"{ssim:.4f}")
            
            messagebox.showinfo("Success", f"Text embedded successfully!\nSaved as: {output_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to embed text: {str(e)}")
            
    def extract_text(self):
        if self.stego_image is None:
            messagebox.showerror("Error", "Please select a stego image first!")
            return
            
        try:
            start_time = time.time()
            
            # Convert to YCrCb
            img_ycrcb = cv2.cvtColor(self.stego_image, cv2.COLOR_BGR2YCrCb)
            y_channel = img_ycrcb[:, :, 0].astype(float)
            
            # Apply DWT
            coeffs = pywt.dwt2(y_channel, 'haar')
            LL, _ = coeffs
            
            # Extract from LL band
            flat_LL = LL.flatten()
            
            # Extract binary text
            binary_text = ''
            for value in flat_LL:
                binary_text += str(int(value) & 1)
                
                # Check for end marker
                if binary_text[-16:] == '1111111111111110':
                    binary_text = binary_text[:-16]
                    break
                    
            # Convert binary to text
            extracted_text = self.binary_to_text(binary_text)
            
            # Display extracted text
            self.extracted_text.delete('1.0', tk.END)
            self.extracted_text.insert('1.0', extracted_text)
            
            # Calculate metrics
            end_time = time.time()
            extract_time = end_time - start_time
            
            # Calculate PSNR if we have original image
            if self.input_image is not None:
                mse = np.mean((self.input_image.astype(float) - self.stego_image.astype(float)) ** 2)
                if mse > 0:
                    psnr = 10 * np.log10(255 * 255 / mse)
                else:
                    psnr = float('inf')
                    
                ssim = self.calculate_ssim(self.input_image, self.stego_image)
            else:
                psnr = 0
                ssim = 0
                
            # Update labels
            self.extract_time_label.config(text=f"{extract_time:.4f} s")
            self.psnr_label.config(text=f"{psnr:.2f} dB")
            self.ssim_extract_label.config(text=f"{ssim:.4f}")
            
            messagebox.showinfo("Success", "Text extracted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract text: {str(e)}")
            
    def calculate_ssim(self, img1, img2):
        # Simplified SSIM calculation
        C1 = 6.5025
        C2 = 58.5225
        
        img1 = img1.astype(np.float64)
        img2 = img2.astype(np.float64)
        
        mu1 = img1.mean()
        mu2 = img2.mean()
        
        sigma1_sq = ((img1 - mu1) ** 2).mean()
        sigma2_sq = ((img2 - mu2) ** 2).mean()
        sigma12 = ((img1 - mu1) * (img2 - mu2)).mean()
        
        ssim = ((2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)) / \
               ((mu1 ** 2 + mu2 ** 2 + C1) * (sigma1_sq + sigma2_sq + C2))
               
        return ssim
    
    def reset_all(self):
        # Clear all images and text
        self.input_image = None
        self.stego_image = None
        self.embedded_image = None
        self.input_image_path = None
        self.stego_image_path = None
        
        # Reset labels
        self.input_image_label.configure(image='', text="No Image Selected")
        self.embedded_image_label.configure(image='', text="Embedded Image Will Appear Here")
        self.stego_image_label.configure(image='', text="No Stego Image Selected")
        
        # Clear text fields
        self.secret_text.delete('1.0', tk.END)
        self.extracted_text.delete('1.0', tk.END)
        
        # Clear parameter labels
        self.embed_time_label.config(text="")
        self.snr_label.config(text="")
        self.ssim_embed_label.config(text="")
        self.extract_time_label.config(text="")
        self.psnr_label.config(text="")
        self.ssim_extract_label.config(text="")
        
        messagebox.showinfo("Reset", "All fields have been reset!")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Set environment variable to suppress Tk deprecation warning
    os.environ['TK_SILENCE_DEPRECATION'] = '1'
    
    app = DWTSteganography()
    app.run()