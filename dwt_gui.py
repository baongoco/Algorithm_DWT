# import sys
# import os
# import datetime
# import hashlib
# import shutil
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# import cv2
# from dwt_algorithm import DWTSteganography

# class DWTSteganographyGUI(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.dwt = DWTSteganography()
#         self.input_image_path = None
#         self.stego_image_path = None
#         self.stego_image_array = None
#         self.is_maximized = False
#         self.initUI()
        
#     def initUI(self):
#         self.setWindowTitle("DWT Based Image Steganography")
#         self.setMinimumSize(1200, 900)
        
#         # Remove default window frame to create custom title bar
#         self.setWindowFlags(Qt.FramelessWindowHint)
        
#         # Modern color scheme
#         self.setStyleSheet("""
#             QMainWindow { 
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #1e3a5f, stop:1 #2c5282);
#                 border: 2px solid #1a202c;
#             }
#         """)
        
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
        
#         main_layout = QVBoxLayout()
#         main_layout.setContentsMargins(0, 0, 0, 0)
#         main_layout.setSpacing(0)
#         central_widget.setLayout(main_layout)
        
#         self.create_custom_title_bar(main_layout)
#         self.create_content_area(main_layout)
        
#     def create_custom_title_bar(self, parent_layout):
#         """Create custom title bar with window controls"""
#         title_bar = QWidget()
#         title_bar.setFixedHeight(60)
#         title_bar.setStyleSheet("""
#             QWidget { 
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
#                     stop:0 #1a365d, stop:1 #2c5282);
#                 border-bottom: 2px solid #4a90e2;
#             }
#             QLabel { color: white; font-size: 20px; font-weight: bold; }
#         """)
        
#         title_layout = QHBoxLayout()
#         title_layout.setContentsMargins(10, 10, 20, 10)
#         title_bar.setLayout(title_layout)
        
#         # Window control buttons on the LEFT
#         self.create_window_controls(title_layout)
        
#         # Add stretch to push title to center
#         title_layout.addStretch()
        
#         # Title in CENTER
#         title_label = QLabel("DWT Based Image Steganography")
#         title_label.setAlignment(Qt.AlignCenter)
#         title_layout.addWidget(title_label)
        
#         # Add stretch to keep title centered
#         title_layout.addStretch()
        
#         # Make title bar draggable
#         title_bar.mousePressEvent = self.title_bar_mouse_press
#         title_bar.mouseMoveEvent = self.title_bar_mouse_move
        
#         parent_layout.addWidget(title_bar)
        
#     def create_window_controls(self, layout):
#         """Create minimize, maximize, close buttons"""
#         button_style = """
#             QPushButton {
#                 background-color: transparent;
#                 border: none;
#                 color: white;
#                 font-size: 16px;
#                 font-weight: bold;
#                 padding: 8px 12px;
#                 margin: 2px;
#             }
#             QPushButton:hover {
#                 background-color: rgba(255,255,255,0.1);
#                 border-radius: 4px;
#             }
#         """
        
#         # Minimize button
#         minimize_btn = QPushButton("−")
#         minimize_btn.setFixedSize(40, 30)
#         minimize_btn.setStyleSheet(button_style)
#         minimize_btn.clicked.connect(self.showMinimized)
#         layout.addWidget(minimize_btn)
        
#         # Maximize/Restore button
#         self.maximize_btn = QPushButton("□")
#         self.maximize_btn.setFixedSize(40, 30)
#         self.maximize_btn.setStyleSheet(button_style)
#         self.maximize_btn.clicked.connect(self.toggle_maximize)
#         layout.addWidget(self.maximize_btn)
        
#         # Close button
#         close_btn = QPushButton("×")
#         close_btn.setFixedSize(40, 30)
#         close_btn.setStyleSheet(button_style + """
#             QPushButton:hover {
#                 background-color: #e53e3e;
#                 border-radius: 4px;
#             }
#         """)
#         close_btn.clicked.connect(self.close)
#         layout.addWidget(close_btn)
        
#     def toggle_maximize(self):
#         """Toggle between maximized and normal window state"""
#         if self.is_maximized:
#             self.showNormal()
#             self.maximize_btn.setText("□")
#             self.is_maximized = False
#         else:
#             self.showMaximized()
#             self.maximize_btn.setText("❐")
#             self.is_maximized = True
            
#     def title_bar_mouse_press(self, event):
#         """Handle mouse press on title bar for dragging"""
#         if event.button() == Qt.LeftButton:
#             self.drag_pos = event.globalPos()
#             event.accept()
            
#     def title_bar_mouse_move(self, event):
#         """Handle mouse move for window dragging"""
#         if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_pos'):
#             self.move(self.pos() + event.globalPos() - self.drag_pos)
#             self.drag_pos = event.globalPos()
#             event.accept()
        
#     def create_content_area(self, parent_layout):
#         """Create main content area with modern styling"""
#         content_widget = QWidget()
#         content_widget.setStyleSheet("""
#             QWidget {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #2d3748, stop:1 #1a202c);
#             }
#         """)
#         content_layout = QVBoxLayout()
#         content_layout.setContentsMargins(20, 20, 20, 20)
#         content_layout.setSpacing(20)
#         content_widget.setLayout(content_layout)
        
#         self.create_embedding_section(content_layout)
#         self.create_extraction_section(content_layout)
        
#         parent_layout.addWidget(content_widget)
        
#     def create_embedding_section(self, parent_layout):
#         """Create embedding section with modern design"""
#         embed_group = QGroupBox("EMBEDDING SIDE")
#         embed_group.setStyleSheet("""
#             QGroupBox {
#                 font-size: 16px; 
#                 font-weight: bold; 
#                 color: #e2e8f0;
#                 border: 2px solid #4a90e2;
#                 border-radius: 12px;
#                 margin-top: 15px; 
#                 padding-top: 15px;
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #2b6cb0, stop:1 #2c5282);
#             }
#             QGroupBox::title {
#                 subcontrol-origin: margin; 
#                 left: 20px;
#                 padding: 0 15px 0 15px; 
#                 color: #ffffff;
#                 background-color: transparent;
#             }
#         """)
        
#         layout = QVBoxLayout()
#         layout.setContentsMargins(15, 25, 15, 15)
#         layout.setSpacing(15)
#         embed_group.setLayout(layout)
        
#         content_row = QWidget()
#         content_layout = QHBoxLayout()
#         content_layout.setSpacing(20)
#         content_row.setLayout(content_layout)
        
#         input_widget = self.create_image_widget("No Image Selected", "Input Image")
#         self.input_image_label = input_widget[0]
#         content_layout.addWidget(input_widget[1])
        
#         text_widget = self.create_text_widget()
#         content_layout.addWidget(text_widget)
        
#         output_widget = self.create_image_widget("Embedded Image Will Appear Here", "Embedded Stego Image")
#         self.embedded_image_label = output_widget[0]
#         content_layout.addWidget(output_widget[1])
        
#         layout.addWidget(content_row)
        
#         button_row = self.create_button_row([
#             ("Browse Input", self.browse_input_image),
#             ("Embedding", self.embed_text),
#             ("Open Stego Folder", self.open_stego_folder)
#         ])
#         layout.addWidget(button_row)
        
#         param_bar = self.create_param_bar([
#             ("Embedding Time:", "embed_time_label"),
#             ("SNR:", "snr_label"), 
#             ("SSIM:", "ssim_embed_label")
#         ])
#         layout.addWidget(param_bar)
        
#         parent_layout.addWidget(embed_group)
        
#     def create_extraction_section(self, parent_layout):
#         """Create extraction section with modern design"""
#         extract_group = QGroupBox("EXTRACTION SIDE")
#         extract_group.setStyleSheet("""
#             QGroupBox {
#                 font-size: 16px; 
#                 font-weight: bold; 
#                 color: #e2e8f0;
#                 border: 2px solid #4a90e2;
#                 border-radius: 12px;
#                 margin-top: 15px; 
#                 padding-top: 15px;
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #2b6cb0, stop:1 #2c5282);
#             }
#             QGroupBox::title {
#                 subcontrol-origin: margin; 
#                 left: 20px;
#                 padding: 0 15px 0 15px; 
#                 color: #ffffff;
#                 background-color: transparent;
#             }
#         """)
        
#         layout = QVBoxLayout()
#         layout.setContentsMargins(15, 25, 15, 15)
#         layout.setSpacing(15)
#         extract_group.setLayout(layout)
        
#         content_row = QWidget()
#         content_layout = QHBoxLayout()
#         content_layout.setSpacing(20)
#         content_row.setLayout(content_layout)
        
#         stego_widget = self.create_image_widget("No Stego Image Selected", "Stego Image")
#         self.stego_image_label = stego_widget[0]
#         content_layout.addWidget(stego_widget[1])
        
#         extract_widget = self.create_extract_text_widget()
#         content_layout.addWidget(extract_widget)
        
#         button_widget = self.create_button_column([
#             ("Browse Stego Image", self.browse_stego_image),
#             ("Detect Steganography", self.detect_steganography),
#             ("Extraction", self.extract_text),
#             ("Reset", self.reset_all),
#             ("Exit", self.close)
#         ])
#         content_layout.addWidget(button_widget)
        
#         layout.addWidget(content_row)
        
#         param_bar = self.create_param_bar([
#             ("Extraction Time:", "extract_time_label"),
#             ("PSNR:", "psnr_label"),
#             ("SSIM:", "ssim_extract_label")
#         ])
#         layout.addWidget(param_bar)
        
#         parent_layout.addWidget(extract_group)
        
#     def create_image_widget(self, placeholder_text, label_text):
#         """Create image display widget with proper aspect ratio"""
#         widget = QWidget()
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignCenter)
#         widget.setLayout(layout)
        
#         image_label = QLabel(placeholder_text)
#         image_label.setFixedSize(300, 300)  # Increased size for better display
#         image_label.setAlignment(Qt.AlignCenter)
#         image_label.setScaledContents(False)  # Prevent scaling issues
#         image_label.setStyleSheet("""
#             QLabel {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #4a5568, stop:1 #2d3748);
#                 border: 2px solid #4a90e2;
#                 border-radius: 8px;
#                 font-size: 12px; 
#                 color: #e2e8f0;
#                 padding: 15px;
#             }
#         """)
#         layout.addWidget(image_label)
        
#         text_label = QLabel(label_text)
#         text_label.setAlignment(Qt.AlignCenter)
#         text_label.setStyleSheet("""
#             font-style: italic; 
#             font-size: 12px; 
#             background-color: transparent; 
#             color: #e2e8f0; 
#             font-weight: bold;
#             padding: 5px;
#         """)
#         layout.addWidget(text_label)
        
#         return image_label, widget
        
#     def create_text_widget(self):
#         """Create secret text input widget with modern styling"""
#         widget = QWidget()
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignCenter)
#         widget.setLayout(layout)
        
#         label = QLabel("Enter Secret Text To Hide")
#         label.setAlignment(Qt.AlignCenter)
#         label.setStyleSheet("""
#             font-size: 12px; 
#             font-weight: bold; 
#             background-color: transparent; 
#             color: #e2e8f0;
#             padding: 5px;
#         """)
#         layout.addWidget(label)
        
#         self.secret_text = QTextEdit()
#         self.secret_text.setFixedSize(320, 220)
#         self.secret_text.setPlainText("Hello This is msg")
#         self.secret_text.setStyleSheet("""
#             QTextEdit {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #4a5568, stop:1 #2d3748);
#                 border: 2px solid #4a90e2;
#                 border-radius: 8px;
#                 font-size: 11px; 
#                 padding: 10px; 
#                 color: #e2e8f0;
#                 selection-background-color: #4a90e2;
#             }
#             QScrollBar:vertical {
#                 background-color: #2d3748;
#                 width: 12px;
#                 border-radius: 6px;
#             }
#             QScrollBar::handle:vertical {
#                 background-color: #4a90e2;
#                 border-radius: 6px;
#             }
#         """)
#         layout.addWidget(self.secret_text)
        
#         return widget
        
#     def create_extract_text_widget(self):
#         """Create extracted text display widget with modern styling"""
#         widget = QWidget()
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignCenter)
#         widget.setLayout(layout)
        
#         label = QLabel("Extracted Secret Text")
#         label.setAlignment(Qt.AlignCenter)
#         label.setStyleSheet("""
#             font-size: 12px; 
#             font-weight: bold; 
#             background-color: transparent; 
#             color: #e2e8f0;
#             padding: 5px;
#         """)
#         layout.addWidget(label)
        
#         self.extracted_text = QTextEdit()
#         self.extracted_text.setFixedSize(320, 220)
#         self.extracted_text.setReadOnly(True)
#         self.extracted_text.setStyleSheet("""
#             QTextEdit {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #4a5568, stop:1 #2d3748);
#                 border: 2px solid #4a90e2;
#                 border-radius: 8px;
#                 font-size: 11px; 
#                 padding: 10px; 
#                 color: #e2e8f0;
#                 selection-background-color: #4a90e2;
#             }
#             QScrollBar:vertical {
#                 background-color: #2d3748;
#                 width: 12px;
#                 border-radius: 6px;
#             }
#             QScrollBar::handle:vertical {
#                 background-color: #4a90e2;
#                 border-radius: 6px;
#             }
#         """)
#         layout.addWidget(self.extracted_text)
        
#         return widget
        
#     def create_button_row(self, buttons):
#         """Create horizontal button row with modern styling"""
#         widget = QWidget()
#         layout = QHBoxLayout()
#         layout.setAlignment(Qt.AlignCenter)
#         layout.setSpacing(15)
#         widget.setLayout(layout)
        
#         for text, callback in buttons:
#             btn = QPushButton(text)
#             if text == "Open Stego Folder":
#                 btn.setFixedSize(140, 45)
#                 btn.setStyleSheet("""
#                     QPushButton {
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #38a169, stop:1 #2f855a);
#                         font-size: 11px; 
#                         font-weight: bold;
#                         border: none;
#                         border-radius: 8px; 
#                         color: white;
#                         padding: 5px;
#                     }
#                     QPushButton:hover { 
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #48bb78, stop:1 #38a169);
#                     }
#                     QPushButton:pressed {
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #2f855a, stop:1 #276749);
#                     }
#                 """)
#             else:
#                 btn.setFixedSize(160, 50)
#                 btn.setStyleSheet("""
#                     QPushButton {
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #4299e1, stop:1 #3182ce);
#                         font-size: 12px; 
#                         font-weight: bold;
#                         border: none;
#                         border-radius: 8px; 
#                         color: white;
#                         padding: 5px;
#                     }
#                     QPushButton:hover { 
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #63b3ed, stop:1 #4299e1);
#                     }
#                     QPushButton:pressed {
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #3182ce, stop:1 #2c5282);
#                     }
#                 """)
#             btn.clicked.connect(callback)
#             layout.addWidget(btn)
            
#         return widget
        
#     def create_button_column(self, buttons):
#         """Create vertical button column with modern styling"""
#         widget = QWidget()
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignCenter)
#         layout.setSpacing(10)
#         widget.setLayout(layout)
        
#         for text, callback in buttons:
#             btn = QPushButton(text)
#             btn.setFixedSize(200, 45)
            
#             if text == "Detect Steganography":
#                 btn.setStyleSheet("""
#                     QPushButton {
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #ed8936, stop:1 #dd6b20);
#                         font-size: 12px; 
#                         font-weight: bold;
#                         border: none;
#                         border-radius: 8px; 
#                         color: white;
#                         padding: 5px;
#                     }
#                     QPushButton:hover { 
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #f6ad55, stop:1 #ed8936);
#                     }
#                     QPushButton:pressed {
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #dd6b20, stop:1 #c05621);
#                     }
#                 """)
#             elif text == "Exit":
#                 btn.setStyleSheet("""
#                     QPushButton {
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #e53e3e, stop:1 #c53030);
#                         font-size: 12px; 
#                         font-weight: bold;
#                         border: none;
#                         border-radius: 8px; 
#                         color: white;
#                         padding: 5px;
#                     }
#                     QPushButton:hover { 
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #fc8181, stop:1 #e53e3e);
#                     }
#                     QPushButton:pressed {
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #c53030, stop:1 #9c2626);
#                     }
#                 """)
#             else:
#                 btn.setStyleSheet("""
#                     QPushButton {
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #4299e1, stop:1 #3182ce);
#                         font-size: 12px; 
#                         font-weight: bold;
#                         border: none;
#                         border-radius: 8px; 
#                         color: white;
#                         padding: 5px;
#                     }
#                     QPushButton:hover { 
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #63b3ed, stop:1 #4299e1);
#                     }
#                     QPushButton:pressed {
#                         background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                             stop:0 #3182ce, stop:1 #2c5282);
#                     }
#                 """)
            
#             btn.clicked.connect(callback)
#             layout.addWidget(btn)
            
#         return widget
        
#     def create_param_bar(self, params):
#         """Create parameter display bar with modern styling"""
#         widget = QWidget()
#         widget.setFixedHeight(50)
#         widget.setStyleSheet("""
#             QWidget {
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
#                     stop:0 #1a365d, stop:1 #2c5282);
#                 border: 1px solid #4a90e2;
#                 border-radius: 8px;
#             }
#         """)
#         layout = QHBoxLayout()
#         layout.setContentsMargins(15, 8, 15, 8)
#         widget.setLayout(layout)
        
#         param_label = QLabel("Parameters")
#         param_label.setStyleSheet("""
#             font-weight: bold; 
#             font-style: italic; 
#             font-size: 13px; 
#             color: #e2e8f0;
#             background-color: transparent;
#         """)
#         layout.addWidget(param_label)
        
#         for label_text, attr_name in params:
#             label = QLabel(label_text)
#             label.setStyleSheet("""
#                 color: #e2e8f0; 
#                 font-size: 11px; 
#                 font-weight: bold;
#                 background-color: transparent;
#             """)
#             layout.addWidget(label)
            
#             value_label = QLabel("")
#             value_label.setFixedWidth(100)
#             value_label.setStyleSheet("""
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #4a5568, stop:1 #2d3748);
#                 border: 1px solid #4a90e2;
#                 border-radius: 4px;
#                 padding: 4px 8px; 
#                 color: #e2e8f0;
#                 font-size: 11px;
#             """)
#             setattr(self, attr_name, value_label)
#             layout.addWidget(value_label)
            
#         layout.addStretch()
#         return widget
        
#     def display_image(self, image_path, label):
#         """Display image in label with proper aspect ratio preservation"""
#         try:
#             pixmap = QPixmap(image_path)
#             if pixmap.isNull():
#                 raise Exception("Invalid image file")
                
#             # Calculate proper scaling to fit within label while maintaining aspect ratio
#             label_size = label.size()
#             # Reduce padding to show more of the image
#             target_size = QSize(label_size.width() - 30, label_size.height() - 30)
            
#             scaled_pixmap = pixmap.scaled(
#                 target_size, 
#                 Qt.KeepAspectRatio, 
#                 Qt.SmoothTransformation
#             )
            
#             label.setPixmap(scaled_pixmap)
#             label.setAlignment(Qt.AlignCenter)
            
#             # Update label style to remove background when image is loaded
#             label.setStyleSheet("""
#                 QLabel {
#                     background: transparent;
#                     border: 2px solid #4a90e2;
#                     border-radius: 8px;
#                     padding: 15px;
#                 }
#             """)
            
#         except Exception as e:
#             label.setText(f"Error loading image:\n{str(e)}")
#             label.setPixmap(QPixmap())
#             # Restore original background for error state
#             label.setStyleSheet("""
#                 QLabel {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                         stop:0 #4a5568, stop:1 #2d3748);
#                     border: 2px solid #4a90e2;
#                     border-radius: 8px;
#                     font-size: 12px; 
#                     color: #e2e8f0;
#                     padding: 15px;
#                 }
#             """)
#             QMessageBox.critical(self, "Error", f"Failed to display image: {str(e)}")
    
#     def browse_input_image(self):
#         """Browse input image"""
#         filename, _ = QFileDialog.getOpenFileName(
#             self, "Select Input Image", "",
#             "Image Files (*.png *.jpg *.jpeg *.bmp)"
#         )
#         if filename:
#             self.input_image_path = filename
#             self.display_image(filename, self.input_image_label)
            
#     def browse_stego_image(self):
#         """Enhanced browse with quick access to stego_images folder"""
#         default_dir = ""
#         if os.path.exists("stego_images"):
#             default_dir = "stego_images"
        
#         filename, _ = QFileDialog.getOpenFileName(
#             self, "Select Stego Image", default_dir,
#             "Image Files (*.png *.jpg *.jpeg *.bmp)"
#         )
#         if filename:
#             self.stego_image_path = filename
#             self.display_image(filename, self.stego_image_label)
#             self.check_metadata(filename)
    
#     def embed_text(self):
#         """ENHANCED: Embed text with unique filename generation"""
#         if not self.input_image_path:
#             QMessageBox.warning(self, "Warning", "Please select an input image first!")
#             return
            
#         secret_text = self.secret_text.toPlainText()
#         if not secret_text:
#             QMessageBox.warning(self, "Warning", "Please enter text to hide!")
#             return
            
#         try:
#             self.stego_image_array, metrics = self.dwt.embed_text(
#                 self.input_image_path, secret_text
#             )
            
#             # Generate unique filename
#             original_name = os.path.splitext(os.path.basename(self.input_image_path))[0]
#             timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#             text_hash = hashlib.md5(secret_text.encode()).hexdigest()[:6]
#             output_filename = f"stego_{original_name}_{timestamp}_{text_hash}.png"
            
#             # Create output directory
#             output_dir = "stego_images"
#             if not os.path.exists(output_dir):
#                 os.makedirs(output_dir)
            
#             output_path = os.path.join(output_dir, output_filename)
            
#             if self.dwt.save_stego_image(self.stego_image_array, output_path):
#                 # Save original copy
#                 original_copy = os.path.join(output_dir, f"original_{original_name}_{timestamp}.png")
#                 shutil.copy2(self.input_image_path, original_copy)
                
#                 # Create metadata file
#                 metadata_file = os.path.join(output_dir, f"metadata_{original_name}_{timestamp}.txt")
#                 with open(metadata_file, 'w') as f:
#                     f.write(f"Original Image: {self.input_image_path}\n")
#                     f.write(f"Stego Image: {output_path}\n")
#                     f.write(f"Secret Text: {secret_text}\n")
#                     f.write(f"Text Length: {len(secret_text)}\n")
#                     f.write(f"Embedding Time: {metrics['embedding_time']:.4f}s\n")
#                     f.write(f"PSNR: {metrics.get('psnr', 'N/A')}\n")
#                     f.write(f"SNR: {metrics['snr']:.2f} dB\n")
#                     f.write(f"SSIM: {metrics['ssim']:.4f}\n")
#                     f.write(f"Created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
#                 self.display_image(output_path, self.embedded_image_label)
                
#                 self.embed_time_label.setText(f"{metrics['embedding_time']:.4f} s")
#                 self.snr_label.setText(f"{metrics['snr']:.2f} dB")
#                 self.ssim_embed_label.setText(f"{metrics['ssim']:.4f}")
                
#                 QMessageBox.information(self, "Success", 
#                     f"Text embedded successfully!\n\n"
#                     f"Files saved in '{output_dir}' folder:\n"
#                     f"• Stego image: {output_filename}\n"
#                     f"• Original copy: original_{original_name}_{timestamp}.png\n"
#                     f"• Metadata: metadata_{original_name}_{timestamp}.txt\n\n"
#                     f"You can now safely embed into other images without losing this one!")
#             else:
#                 QMessageBox.critical(self, "Error", "Failed to save stego image!")
                
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Embedding failed: {str(e)}")
    
#     def detect_steganography(self):
#         """Detect if selected image contains steganography"""
#         if not self.stego_image_path:
#             QMessageBox.warning(self, "Warning", "Please select an image to analyze first!")
#             return
        
#         try:
#             is_stego, confidence, details = self.dwt.detect_steganography(self.stego_image_path)
            
#             status = "POSITIVE" if is_stego else "NEGATIVE"
#             message = f"Steganography Detection: {status}\n"
#             message += f"Confidence: {confidence}%\n\n"
            
#             if details:
#                 message += "Analysis Details:\n"
#                 for detail in details:
#                     message += f"• {detail}\n"
#             else:
#                 message += "No suspicious patterns detected."
            
#             if is_stego:
#                 message += "\n" + "="*40 + "\n"
#                 message += "Attempting automatic extraction...\n"
                
#                 try:
#                     extracted_text, _ = self.dwt.extract_text(self.stego_image_path)
#                     if extracted_text and len(extracted_text.strip()) > 0:
#                         message += f"SUCCESS: Found hidden text!\n"
#                         message += f"Extracted: '{extracted_text}'"
#                         self.extracted_text.setPlainText(extracted_text)
#                     else:
#                         message += "No valid text could be extracted."
#                 except Exception as e:
#                     message += f"Extraction failed: {e}"
            
#             self.show_detection_results(status, message)
            
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Detection failed: {str(e)}")
    
#     def show_detection_results(self, status, message):
#         """Show detection results in a custom dialog with modern styling"""
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Steganography Detection Results")
#         dialog.setFixedSize(650, 450)
#         dialog.setStyleSheet("""
#             QDialog {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #2d3748, stop:1 #1a202c);
#                 color: #e2e8f0;
#             }
#         """)
        
#         layout = QVBoxLayout()
        
#         status_label = QLabel(f"Detection Status: {status}")
#         status_label.setAlignment(Qt.AlignCenter)
#         if status == "POSITIVE":
#             status_label.setStyleSheet("""
#                 font-size: 16px; font-weight: bold; 
#                 color: #ffffff; 
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #e53e3e, stop:1 #c53030);
#                 padding: 15px; 
#                 border-radius: 8px; 
#                 margin: 10px;
#                 border: 2px solid #fc8181;
#             """)
#         else:
#             status_label.setStyleSheet("""
#                 font-size: 16px; font-weight: bold; 
#                 color: #ffffff; 
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #38a169, stop:1 #2f855a);
#                 padding: 15px; 
#                 border-radius: 8px; 
#                 margin: 10px;
#                 border: 2px solid #68d391;
#             """)
#         layout.addWidget(status_label)
        
#         text_area = QTextEdit()
#         text_area.setPlainText(message)
#         text_area.setReadOnly(True)
#         text_area.setStyleSheet("""
#             QTextEdit {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #4a5568, stop:1 #2d3748);
#                 border: 2px solid #4a90e2;
#                 border-radius: 8px;
#                 font-family: 'Courier New'; 
#                 font-size: 11px;
#                 padding: 15px;
#                 color: #e2e8f0;
#                 selection-background-color: #4a90e2;
#             }
#             QScrollBar:vertical {
#                 background-color: #2d3748;
#                 width: 12px;
#                 border-radius: 6px;
#             }
#             QScrollBar::handle:vertical {
#                 background-color: #4a90e2;
#                 border-radius: 6px;
#             }
#         """)
#         layout.addWidget(text_area)
        
#         close_btn = QPushButton("Close")
#         close_btn.setFixedSize(120, 35)
#         close_btn.setStyleSheet("""
#             QPushButton {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #4299e1, stop:1 #3182ce);
#                 font-size: 12px; 
#                 font-weight: bold;
#                 border: none;
#                 border-radius: 6px; 
#                 color: white;
#                 padding: 5px;
#             }
#             QPushButton:hover { 
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #63b3ed, stop:1 #4299e1);
#             }
#         """)
#         close_btn.clicked.connect(dialog.close)
#         close_layout = QHBoxLayout()
#         close_layout.addStretch()
#         close_layout.addWidget(close_btn)
#         close_layout.addStretch()
#         layout.addLayout(close_layout)
        
#         dialog.setLayout(layout)
#         dialog.exec_()
            
#     def extract_text(self):
#         """Extract text from stego image"""
#         if not self.stego_image_path:
#             QMessageBox.warning(self, "Warning", "Please select a stego image first!")
#             return
            
#         try:
#             extracted_text, extraction_time = self.dwt.extract_text(self.stego_image_path)
            
#             self.extracted_text.setPlainText(extracted_text)
            
#             self.extract_time_label.setText(f"{extraction_time:.4f} s")
            
#             if self.input_image_path:
#                 original = cv2.imread(self.input_image_path)
#                 stego = cv2.imread(self.stego_image_path)
#                 metrics = self.dwt.calculate_metrics(original, stego)
                
#                 self.psnr_label.setText(f"{metrics['psnr']:.2f} dB")
#                 self.ssim_extract_label.setText(f"{metrics['ssim']:.4f}")
            
#             # Modern success dialog
#             msg = QMessageBox(self)
#             msg.setWindowTitle("Extraction Success")
#             msg.setText(f"Text extracted successfully!\n\nExtracted text: '{extracted_text}'")
#             msg.setStyleSheet("""
#                 QMessageBox {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                         stop:0 #2d3748, stop:1 #1a202c);
#                     color: #e2e8f0;
#                 }
#                 QMessageBox QPushButton {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                         stop:0 #4299e1, stop:1 #3182ce);
#                     color: white;
#                     border: none;
#                     padding: 8px 16px;
#                     border-radius: 4px;
#                     font-weight: bold;
#                 }
#             """)
#             msg.exec_()
            
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Extraction failed: {str(e)}")
    
#     def check_metadata(self, image_path):
#         """Check if metadata file exists for selected image"""
#         try:
#             filename = os.path.basename(image_path)
#             if filename.startswith("stego_"):
#                 base_name = filename.replace("stego_", "").replace(".png", "")
#                 metadata_file = os.path.join(os.path.dirname(image_path), f"metadata_{base_name}.txt")
                
#                 if os.path.exists(metadata_file):
#                     with open(metadata_file, 'r') as f:
#                         metadata_content = f.read()
                    
#                     # Modern metadata dialog
#                     msg = QMessageBox(self)
#                     msg.setWindowTitle("Image Metadata Found")
#                     msg.setText(f"Found metadata for this image:\n\n{metadata_content}")
#                     msg.setStyleSheet("""
#                         QMessageBox {
#                             background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                 stop:0 #2d3748, stop:1 #1a202c);
#                             color: #e2e8f0;
#                         }
#                         QMessageBox QPushButton {
#                             background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                 stop:0 #4299e1, stop:1 #3182ce);
#                             color: white;
#                             border: none;
#                             padding: 8px 16px;
#                             border-radius: 4px;
#                             font-weight: bold;
#                         }
#                     """)
#                     msg.exec_()
#         except Exception as e:
#             pass
    
#     def open_stego_folder(self):
#         """Open the stego_images folder"""
#         if not os.path.exists("stego_images"):
#             os.makedirs("stego_images")
            
#         try:
#             if sys.platform == "darwin":  # macOS
#                 os.system(f"open {'stego_images'}")
#             elif sys.platform == "win32":  # Windows
#                 os.system(f"explorer {'stego_images'}")
#             else:  # Linux
#                 os.system(f"xdg-open {'stego_images'}")
#         except Exception as e:
#             msg = QMessageBox(self)
#             msg.setWindowTitle("Folder Location")
#             msg.setText(f"Stego images folder location:\n{os.path.abspath('stego_images')}")
#             msg.setStyleSheet("""
#                 QMessageBox {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                         stop:0 #2d3748, stop:1 #1a202c);
#                     color: #e2e8f0;
#                 }
#                 QMessageBox QPushButton {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                         stop:0 #4299e1, stop:1 #3182ce);
#                     color: white;
#                     border: none;
#                     padding: 8px 16px;
#                     border-radius: 4px;
#                     font-weight: bold;
#                 }
#             """)
#             msg.exec_()
            
#     def reset_all(self):
#         """Reset all fields"""
#         self.input_image_path = None
#         self.stego_image_path = None
#         self.stego_image_array = None
        
#         self.input_image_label.clear()
#         self.input_image_label.setText("No Image Selected")
#         self.embedded_image_label.clear()
#         self.embedded_image_label.setText("Embedded Image Will Appear Here")
#         self.stego_image_label.clear()
#         self.stego_image_label.setText("No Stego Image Selected")
        
#         self.secret_text.setPlainText("Hello This is msg")
#         self.extracted_text.clear()
        
#         for attr in ['embed_time_label', 'snr_label', 'ssim_embed_label',
#                      'extract_time_label', 'psnr_label', 'ssim_extract_label']:
#             getattr(self, attr).clear()
        
#         # Modern reset confirmation
#         msg = QMessageBox(self)
#         msg.setWindowTitle("Reset Complete")
#         msg.setText("All fields have been reset!")
#         msg.setStyleSheet("""
#             QMessageBox {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #2d3748, stop:1 #1a202c);
#                 color: #e2e8f0;
#             }
#             QMessageBox QPushButton {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                     stop:0 #38a169, stop:1 #2f855a);
#                 color: white;
#                 border: none;
#                 padding: 8px 16px;
#                 border-radius: 4px;
#                 font-weight: bold;
#             }
#         """)
#         msg.exec_()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
    
#     # Set application-wide style
#     app.setStyleSheet("""
#         QMessageBox {
#             background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                 stop:0 #2d3748, stop:1 #1a202c);
#             color: #e2e8f0;
#             border: 2px solid #4a90e2;
#             border-radius: 8px;
#         }
#         QMessageBox QPushButton {
#             background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                 stop:0 #4299e1, stop:1 #3182ce);
#             color: white;
#             border: none;
#             padding: 8px 16px;
#             border-radius: 4px;
#             font-weight: bold;
#             min-width: 80px;
#         }
#         QMessageBox QPushButton:hover {
#             background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                 stop:0 #63b3ed, stop:1 #4299e1);
#         }
#         QFileDialog {
#             background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                 stop:0 #2d3748, stop:1 #1a202c);
#             color: #e2e8f0;
#         }
#     """)
    
#     window = DWTSteganographyGUI()
#     window.show()
#     sys.exit(app.exec_())

# dwt_gui.py - Updated for True DWT Steganography Algorithm
import sys
import os
import datetime
import hashlib
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from dwt_algorithm import DWTSteganography

class HistogramWidget(QWidget):
    """Enhanced histogram widget for DWT analysis"""
    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        # Dark theme for matplotlib
        self.figure.patch.set_facecolor('#2d3748')
        
    def plot_dwt_analysis(self, image_path, title="DWT Coefficient Analysis"):
        """Plot DWT coefficient analysis"""
        try:
            self.figure.clear()
            
            image = cv2.imread(image_path)
            if image is None:
                return False
            
            # Create 2x3 subplot layout
            axes = self.figure.subplots(2, 3, figsize=(12, 8))
            self.figure.suptitle(title, fontsize=14, color='white', y=0.95)
            
            colors = ['#3b82f6', '#10b981', '#ef4444']
            channel_names = ['Blue', 'Green', 'Red']
            
            import pywt
            
            for i in range(3):
                channel = image[:, :, i].astype(np.float64)
                
                # Apply 2-level DWT (same as algorithm)
                coeffs2 = pywt.wavedec2(channel, 'haar', level=2)
                cA2 = coeffs2[0]  # Approximation
                cH2, cV2, cD2 = coeffs2[1]  # Level 2 details
                
                # Plot coefficient histograms
                # Top row: Mid-frequency coefficients (embedding location)
                cH2_flat = cH2.flatten()
                axes[0, i].hist(cH2_flat, bins=50, alpha=0.7, color=colors[i], density=True)
                axes[0, i].set_title(f'{channel_names[i]} - Mid-Freq Coeffs (cH2)', 
                                   color='white', fontsize=10)
                axes[0, i].tick_params(colors='white', labelsize=8)
                axes[0, i].set_facecolor('#1a202c')
                axes[0, i].grid(True, alpha=0.3, color='white')
                
                # Bottom row: Approximation coefficients  
                cA2_flat = cA2.flatten()
                axes[1, i].hist(cA2_flat, bins=50, alpha=0.7, color=colors[i], density=True)
                axes[1, i].set_title(f'{channel_names[i]} - Low-Freq Coeffs (cA2)', 
                                   color='white', fontsize=10)
                axes[1, i].tick_params(colors='white', labelsize=8)
                axes[1, i].set_facecolor('#1a202c')
                axes[1, i].grid(True, alpha=0.3, color='white')
                
                # Add statistics
                mean_cH2 = np.mean(cH2_flat)
                std_cH2 = np.std(cH2_flat)
                axes[0, i].axvline(mean_cH2, color='red', linestyle='--', alpha=0.8)
                axes[0, i].text(0.02, 0.95, f'μ={mean_cH2:.2f}\nσ={std_cH2:.2f}', 
                              transform=axes[0, i].transAxes, verticalalignment='top',
                              color='white', fontsize=8,
                              bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
            
            self.figure.tight_layout()
            self.canvas.draw()
            return True
            
        except Exception as e:
            print(f"DWT analysis plotting error: {e}")
            return False
    
    def plot_histogram_comparison(self, original_path, stego_path):
        """Enhanced comparison with DWT focus"""
        try:
            self.figure.clear()
            
            original = cv2.imread(original_path)
            stego = cv2.imread(stego_path)
            
            if original is None or stego is None:
                return False
            
            # 3x3 layout: Histograms + DWT analysis
            axes = self.figure.subplots(3, 3, figsize=(12, 10))
            self.figure.suptitle('DWT Steganography: Original vs Stego Analysis', 
                               fontsize=14, color='white', y=0.95)
            
            colors = ['#3b82f6', '#10b981', '#ef4444']
            channel_names = ['Blue (Embed)', 'Green', 'Red']
            
            import pywt
            
            for i in range(3):
                # Row 1: Original histograms
                hist_orig = cv2.calcHist([original], [i], None, [256], [0, 256])
                axes[0, i].plot(hist_orig, color=colors[i], alpha=0.8, linewidth=1.5)
                axes[0, i].set_title(f'Original - {channel_names[i]}', 
                                   color='white', fontsize=10)
                axes[0, i].set_facecolor('#1a202c')
                axes[0, i].tick_params(colors='white', labelsize=8)
                axes[0, i].grid(True, alpha=0.3, color='white')
                
                # Row 2: Stego histograms
                hist_stego = cv2.calcHist([stego], [i], None, [256], [0, 256])
                axes[1, i].plot(hist_stego, color=colors[i], alpha=0.8, linewidth=1.5)
                axes[1, i].set_title(f'Stego - {channel_names[i]}', 
                                   color='white', fontsize=10)
                axes[1, i].set_facecolor('#1a202c')
                axes[1, i].tick_params(colors='white', labelsize=8)
                axes[1, i].grid(True, alpha=0.3, color='white')
                
                # Row 3: DWT coefficient differences
                orig_channel = original[:, :, i].astype(np.float64)
                stego_channel = stego[:, :, i].astype(np.float64)
                
                # DWT analysis
                orig_coeffs2 = pywt.wavedec2(orig_channel, 'haar', level=2)
                stego_coeffs2 = pywt.wavedec2(stego_channel, 'haar', level=2)
                
                # Compare mid-frequency coefficients (embedding location)
                orig_cH2 = orig_coeffs2[1][0].flatten()  # cH2
                stego_cH2 = stego_coeffs2[1][0].flatten()  # cH2
                
                coeff_diff = np.abs(orig_cH2 - stego_cH2)
                axes[2, i].hist(coeff_diff, bins=30, alpha=0.7, color='orange', density=True)
                axes[2, i].set_title(f'DWT Coeff Diff - {channel_names[i]}', 
                                   color='white', fontsize=10)
                axes[2, i].set_facecolor('#1a202c')
                axes[2, i].tick_params(colors='white', labelsize=8)
                axes[2, i].grid(True, alpha=0.3, color='white')
                
                # Add statistics
                max_diff = np.max(coeff_diff)
                mean_diff = np.mean(coeff_diff)
                axes[2, i].text(0.02, 0.95, f'Max: {max_diff:.3f}\nMean: {mean_diff:.4f}', 
                              transform=axes[2, i].transAxes, verticalalignment='top',
                              color='white', fontsize=8,
                              bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
                
                # Highlight embedding channel
                if i == 0:  # Blue channel
                    axes[2, i].set_ylabel('Density (EMBEDDING CHANNEL)', color='yellow', fontweight='bold')
            
            self.figure.tight_layout()
            self.canvas.draw()
            return True
            
        except Exception as e:
            print(f"DWT comparison plotting error: {e}")
            return False

class DWTSteganographyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dwt = DWTSteganography()
        self.input_image_path = None
        self.stego_image_path = None
        self.stego_image_array = None
        self.is_maximized = False
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("True DWT Steganography with Advanced Analysis")
        self.setMinimumSize(1400, 1000)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Enhanced dark theme
        self.setStyleSheet("""
            QMainWindow { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a365d, stop:1 #2c5282);
                border: 2px solid #1a202c;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        
        self.create_custom_title_bar(main_layout)
        self.create_content_area(main_layout)
        
    def create_custom_title_bar(self, parent_layout):
        """Enhanced title bar with DWT info"""
        title_bar = QWidget()
        title_bar.setFixedHeight(60)
        title_bar.setStyleSheet("""
            QWidget { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a365d, stop:1 #2c5282);
                border-bottom: 2px solid #4a90e2;
            }
        """)
        
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 5, 20, 5)
        title_bar.setLayout(title_layout)
        
        # Window controls
        self.create_window_controls(title_layout)
        title_layout.addStretch()
        
        # Enhanced title with algorithm info
        title_widget = QWidget()
        title_widget_layout = QVBoxLayout()
        title_widget_layout.setContentsMargins(0, 0, 0, 0)
        title_widget_layout.setSpacing(2)
        
        main_title = QLabel("True DWT Steganography System")
        main_title.setAlignment(Qt.AlignCenter)
        main_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        
        sub_title = QLabel("2-Level DWT • Mid-Frequency Embedding • Quantization-Based • Blue Channel")
        sub_title.setAlignment(Qt.AlignCenter)
        sub_title.setStyleSheet("color: #a0aec0; font-size: 10px; font-style: italic;")
        
        title_widget_layout.addWidget(main_title)
        title_widget_layout.addWidget(sub_title)
        title_widget.setLayout(title_widget_layout)
        
        title_layout.addWidget(title_widget)
        title_layout.addStretch()
        
        # Algorithm info
        algo_info = QLabel(f"Wavelet: {self.dwt.wavelet.upper()} • Strength: {self.dwt.embedding_strength}")
        algo_info.setStyleSheet("color: #68d391; font-size: 9px; font-weight: bold;")
        title_layout.addWidget(algo_info)
        
        title_bar.mousePressEvent = self.title_bar_mouse_press
        title_bar.mouseMoveEvent = self.title_bar_mouse_move
        
        parent_layout.addWidget(title_bar)
        
    def create_window_controls(self, layout):
        """Window control buttons"""
        button_style = """
            QPushButton {
                background-color: transparent; border: none; color: white;
                font-size: 16px; font-weight: bold; padding: 8px 12px; margin: 2px;
            }
            QPushButton:hover { background-color: rgba(255,255,255,0.1); border-radius: 4px; }
        """
        
        minimize_btn = QPushButton("−")
        minimize_btn.setFixedSize(40, 30)
        minimize_btn.setStyleSheet(button_style)
        minimize_btn.clicked.connect(self.showMinimized)
        layout.addWidget(minimize_btn)
        
        self.maximize_btn = QPushButton("□")
        self.maximize_btn.setFixedSize(40, 30)
        self.maximize_btn.setStyleSheet(button_style)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.maximize_btn)
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(40, 30)
        close_btn.setStyleSheet(button_style + """
            QPushButton:hover { background-color: #e53e3e; border-radius: 4px; }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
    def toggle_maximize(self):
        if self.is_maximized:
            self.showNormal()
            self.maximize_btn.setText("□")
            self.is_maximized = False
        else:
            self.showMaximized()
            self.maximize_btn.setText("❐")
            self.is_maximized = True
            
    def title_bar_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()
            
    def title_bar_mouse_move(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_pos'):
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()
        
    def create_content_area(self, parent_layout):
        """Enhanced content with DWT-specific info"""
        content_widget = QWidget()
        content_widget.setStyleSheet("""
            QWidget { background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2d3748, stop:1 #1a202c); }
        """)
        
        # Horizontal splitter
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setStyleSheet("""
            QSplitter::handle { background-color: #4a90e2; width: 3px; border-radius: 1px; }
        """)
        
        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(15)
        left_panel.setLayout(left_layout)
        
        self.create_embedding_section(left_layout)
        self.create_extraction_section(left_layout)
        
        # Right panel - DWT Analysis
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(15, 15, 15, 15)
        right_panel.setLayout(right_layout)
        
        self.create_dwt_analysis_section(right_layout)
        
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setStretchFactor(0, 2)
        main_splitter.setStretchFactor(1, 1)
        
        content_layout = QVBoxLayout()
        content_layout.addWidget(main_splitter)
        content_widget.setLayout(content_layout)
        
        parent_layout.addWidget(content_widget)
        
    def create_dwt_analysis_section(self, parent_layout):
        """Enhanced DWT-specific analysis section"""
        dwt_group = QGroupBox("DWT COEFFICIENT ANALYSIS")
        dwt_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px; font-weight: bold; color: #e2e8f0;
                border: 2px solid #ed8936; border-radius: 12px;
                margin-top: 15px; padding-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c05621, stop:1 #9c4221);
            }
            QGroupBox::title {
                subcontrol-origin: margin; left: 20px;
                padding: 0 15px 0 15px; color: #ffffff;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 10)
        dwt_group.setLayout(layout)
        
        # DWT visualization widget
        self.dwt_widget = HistogramWidget()
        self.dwt_widget.setMinimumHeight(450)
        layout.addWidget(self.dwt_widget)
        
        # Enhanced control buttons
        button_layout = QHBoxLayout()
        
        self.show_orig_dwt_btn = QPushButton("Original DWT")
        self.show_orig_dwt_btn.setStyleSheet(self.get_dwt_button_style())
        self.show_orig_dwt_btn.clicked.connect(self.show_original_dwt)
        button_layout.addWidget(self.show_orig_dwt_btn)
        
        self.show_stego_dwt_btn = QPushButton("Stego DWT")
        self.show_stego_dwt_btn.setStyleSheet(self.get_dwt_button_style())
        self.show_stego_dwt_btn.clicked.connect(self.show_stego_dwt)
        button_layout.addWidget(self.show_stego_dwt_btn)
        
        self.compare_dwt_btn = QPushButton("Compare DWT")
        self.compare_dwt_btn.setStyleSheet(self.get_dwt_button_style('#38a169'))
        self.compare_dwt_btn.clicked.connect(self.compare_dwt_analysis)
        button_layout.addWidget(self.compare_dwt_btn)
        
        layout.addLayout(button_layout)
        
        # Enhanced analysis results with DWT metrics
        self.dwt_analysis = QTextEdit()
        self.dwt_analysis.setFixedHeight(140)
        self.dwt_analysis.setReadOnly(True)
        self.dwt_analysis.setPlaceholderText("DWT coefficient analysis results will appear here...")
        self.dwt_analysis.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a5568, stop:1 #2d3748);
                border: 2px solid #ed8936; border-radius: 8px;
                font-size: 10px; padding: 8px; color: #e2e8f0;
                font-family: 'Courier New';
            }
        """)
        layout.addWidget(self.dwt_analysis)
        
        parent_layout.addWidget(dwt_group)
        
    def get_dwt_button_style(self, color='#ed8936'):
        """Enhanced button styles"""
        hover_color = '#f6ad55' if color == '#ed8936' else '#48bb78'
        pressed_color = '#dd6b20' if color == '#ed8936' else '#2f855a'
        
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color}, stop:1 {pressed_color});
                font-size: 10px; font-weight: bold; border: none;
                border-radius: 6px; color: white; padding: 8px 12px; margin: 2px;
            }}
            QPushButton:hover {{ 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {hover_color}, stop:1 {color});
            }}
        """
        
    def show_original_dwt(self):
        """Show DWT coefficient analysis of original image"""
        if not self.input_image_path:
            QMessageBox.warning(self, "Warning", "Please select an input image first!")
            return
        
        success = self.dwt_widget.plot_dwt_analysis(
            self.input_image_path, "Original Image - DWT Coefficient Analysis"
        )
        if success:
            self.dwt_analysis.setText(
                f"Original Image DWT Analysis:\n"
                f"Image: {os.path.basename(self.input_image_path)}\n"
                f"Decomposition: 2-level DWT using {self.dwt.wavelet.upper()} wavelet\n"
                f"Coefficients: cA2 (approx), cH2/cV2/cD2 (level-2), cH1/cV1/cD1 (level-1)\n"
                f"Analysis: Displaying coefficient distributions for baseline comparison\n"
                f"Blue Channel: Target for steganography embedding\n"
                f"Mid-Frequency (cH2): Embedding location for robustness vs imperceptibility"
            )
    
    def show_stego_dwt(self):
        """Show DWT analysis of stego image with detection"""
        if not self.stego_image_path:
            QMessageBox.warning(self, "Warning", "Please select a stego image first!")
            return
        
        success = self.dwt_widget.plot_dwt_analysis(
            self.stego_image_path, "Stego Image - DWT Coefficient Analysis"
        )
        if success:
            # Perform DWT-specific analysis
            try:
                analysis_result = self.dwt.analyze_image(self.stego_image_path)
                
                is_suspicious = analysis_result['is_suspicious']
                confidence = analysis_result['confidence']
                details = analysis_result['details']
                
                analysis_text = f"Stego Image DWT Analysis:\n"
                analysis_text += f"Image: {os.path.basename(self.stego_image_path)}\n"
                analysis_text += f"Detection Confidence: {confidence:.1f}%\n"
                analysis_text += f"Status: {'SUSPICIOUS' if is_suspicious else 'NORMAL'}\n\n"
                
                if details:
                    analysis_text += "DWT Detection Results:\n"
                    for detail in details[:3]:  # Show top 3 details
                        analysis_text += f"• {detail}\n"
                
                if is_suspicious:
                    analysis_text += f"\n⚠️ ALERT: DWT patterns suggest steganography!\n"
                    analysis_text += f"Recommended: Check blue channel mid-frequency coefficients"
                else:
                    analysis_text += f"\n✓ Normal DWT coefficient distribution detected"
                
                self.dwt_analysis.setText(analysis_text)
                
            except Exception as e:
                self.dwt_analysis.setText(f"DWT analysis error: {str(e)}")
    
    def compare_dwt_analysis(self):
        """Compare DWT coefficients between original and stego"""
        if not self.input_image_path or not self.stego_image_path:
            QMessageBox.warning(self, "Warning", 
                "Please select both original and stego images!")
            return
        
        success = self.dwt_widget.plot_histogram_comparison(
            self.input_image_path, self.stego_image_path
        )
        
        if success:
            # Perform detailed DWT comparison
            try:
                import pywt
                
                original = cv2.imread(self.input_image_path).astype(np.float64)
                stego = cv2.imread(self.stego_image_path).astype(np.float64)
                
                analysis_text = f"DWT Comparative Analysis:\n"
                analysis_text += f"Original: {os.path.basename(self.input_image_path)}\n"
                analysis_text += f"Stego: {os.path.basename(self.stego_image_path)}\n\n"
                
                # Analyze each channel's DWT coefficients
                for i, channel_name in enumerate(['Blue (EMBED)', 'Green', 'Red']):
                    orig_channel = original[:, :, i]
                    stego_channel = stego[:, :, i]
                    
                    # 2-level DWT
                    orig_coeffs2 = pywt.wavedec2(orig_channel, 'haar', level=2)
                    stego_coeffs2 = pywt.wavedec2(stego_channel, 'haar', level=2)
                    
                    # Compare mid-frequency coefficients (embedding location)
                    orig_cH2 = orig_coeffs2[1][0].flatten()
                    stego_cH2 = stego_coeffs2[1][0].flatten()
                    
                    # Calculate differences
                    coeff_diff = np.abs(orig_cH2 - stego_cH2)
                    max_diff = np.max(coeff_diff)
                    mean_diff = np.mean(coeff_diff)
                    modified_coeffs = np.sum(coeff_diff > 0.001)
                    
                    analysis_text += f"{channel_name} Channel (cH2 coefficients):\n"
                    analysis_text += f"  Max Difference: {max_diff:.4f}\n"
                    analysis_text += f"  Mean Difference: {mean_diff:.4f}\n"
                    analysis_text += f"  Modified Coeffs: {modified_coeffs}/{len(orig_cH2)}\n"
                    
                    if i == 0:  # Blue channel (embedding channel)
                        if mean_diff > 0.01:
                            analysis_text += f"  🚨 SIGNIFICANT CHANGES in embedding channel!\n"
                        else:
                            analysis_text += f"  ✓ Minimal changes (good imperceptibility)\n"
                    
                    analysis_text += "\n"
                
                self.dwt_analysis.setText(analysis_text)
                
            except Exception as e:
                self.dwt_analysis.setText(f"DWT comparison error: {str(e)}")
    
    def create_embedding_section(self, parent_layout):
        """Enhanced embedding section with DWT metrics"""
        embed_group = QGroupBox("DWT EMBEDDING")
        embed_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px; font-weight: bold; color: #e2e8f0;
                border: 2px solid #4a90e2; border-radius: 12px;
                margin-top: 15px; padding-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2b6cb0, stop:1 #2c5282);
            }
            QGroupBox::title {
                subcontrol-origin: margin; left: 20px;
                padding: 0 15px 0 15px; color: #ffffff;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 10)
        layout.setSpacing(12)
        embed_group.setLayout(layout)
        
        content_row = QWidget()
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        content_row.setLayout(content_layout)
        
        input_widget = self.create_image_widget("No Image Selected", "Input Image", size=(200, 200))
        self.input_image_label = input_widget[0]
        content_layout.addWidget(input_widget[1])
        
        text_widget = self.create_text_widget(size=(220, 150))
        content_layout.addWidget(text_widget)
        
        output_widget = self.create_image_widget("DWT Stego Image", "Stego Image", size=(200, 200))
        self.embedded_image_label = output_widget[0]
        content_layout.addWidget(output_widget[1])
        
        layout.addWidget(content_row)
        
        button_row = self.create_button_row([
            ("Browse Input", self.browse_input_image),
            ("DWT Embed", self.embed_text),
            ("Open Folder", self.open_stego_folder)
        ])
        layout.addWidget(button_row)
        
        # Enhanced metrics bar with DWT-specific metrics
        param_bar = self.create_param_bar([
            ("Time:", "embed_time_label"),
            ("PSNR:", "embed_psnr_label"), 
            ("SSIM:", "ssim_embed_label"),
            ("Capacity:", "capacity_label"),
            ("Wavelet:", "wavelet_label")
        ])
        layout.addWidget(param_bar)
        
        parent_layout.addWidget(embed_group)
        
    def create_extraction_section(self, parent_layout):
        """Enhanced extraction section with DWT detection"""
        extract_group = QGroupBox("DWT EXTRACTION & DETECTION")
        extract_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px; font-weight: bold; color: #e2e8f0;
                border: 2px solid #4a90e2; border-radius: 12px;
                margin-top: 15px; padding-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2b6cb0, stop:1 #2c5282);
            }
            QGroupBox::title {
                subcontrol-origin: margin; left: 20px;
                padding: 0 15px 0 15px; color: #ffffff;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 10)
        layout.setSpacing(12)
        extract_group.setLayout(layout)
        
        content_row = QWidget()
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        content_row.setLayout(content_layout)
        
        stego_widget = self.create_image_widget("No Stego Image", "Stego Image", size=(200, 200))
        self.stego_image_label = stego_widget[0]
        content_layout.addWidget(stego_widget[1])
        
        extract_widget = self.create_extract_text_widget(size=(220, 150))
        content_layout.addWidget(extract_widget)
        
        button_widget = self.create_button_column([
            ("Browse Stego", self.browse_stego_image),
            ("DWT Detect", self.detect_steganography),
            ("DWT Extract", self.extract_text),
            ("Reset All", self.reset_all),
            ("Exit", self.close)
        ])
        content_layout.addWidget(button_widget)
        
        layout.addWidget(content_row)
        
        # Enhanced metrics with DWT detection info
        param_bar = self.create_param_bar([
            ("Extract Time:", "extract_time_label"),
            ("Detection:", "detection_label"),
            ("Confidence:", "confidence_label"),
            ("Method:", "method_label")
        ])
        layout.addWidget(param_bar)
        
        parent_layout.addWidget(extract_group)
        
    def create_image_widget(self, placeholder_text, label_text, size=(300, 300)):
        """Create image display widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        widget.setLayout(layout)
        
        image_label = QLabel(placeholder_text)
        image_label.setFixedSize(size[0], size[1])
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setScaledContents(False)
        image_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a5568, stop:1 #2d3748);
                border: 2px solid #4a90e2; border-radius: 8px;
                font-size: 11px; color: #e2e8f0; padding: 10px;
            }
        """)
        layout.addWidget(image_label)
        
        text_label = QLabel(label_text)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("""
            font-size: 11px; font-weight: bold; 
            color: #e2e8f0; padding: 5px;
        """)
        layout.addWidget(text_label)
        
        return image_label, widget
        
    def create_text_widget(self, size=(320, 220)):
        """Create text input widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        widget.setLayout(layout)
        
        label = QLabel("Secret Text (UTF-8 Support)")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            font-size: 11px; font-weight: bold; 
            color: #e2e8f0; padding: 5px;
        """)
        layout.addWidget(label)
        
        self.secret_text = QTextEdit()
        self.secret_text.setFixedSize(size[0], size[1])
        self.secret_text.setPlainText("Hello DWT Steganography! 🔐")
        self.secret_text.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a5568, stop:1 #2d3748);
                border: 2px solid #4a90e2; border-radius: 8px;
                font-size: 10px; padding: 8px; color: #e2e8f0;
            }
        """)
        layout.addWidget(self.secret_text)
        
        return widget
        
    def create_extract_text_widget(self, size=(320, 220)):
        """Create extracted text widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        widget.setLayout(layout)
        
        label = QLabel("Extracted Text")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            font-size: 11px; font-weight: bold; 
            color: #e2e8f0; padding: 5px;
        """)
        layout.addWidget(label)
        
        self.extracted_text = QTextEdit()
        self.extracted_text.setFixedSize(size[0], size[1])
        self.extracted_text.setReadOnly(True)
        self.extracted_text.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a5568, stop:1 #2d3748);
                border: 2px solid #4a90e2; border-radius: 8px;
                font-size: 10px; padding: 8px; color: #e2e8f0;
            }
        """)
        layout.addWidget(self.extracted_text)
        
        return widget
        
    def create_button_row(self, buttons):
        """Create button row"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        widget.setLayout(layout)
        
        for text, callback in buttons:
            btn = QPushButton(text)
            if "Folder" in text:
                btn.setFixedSize(100, 35)
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #38a169, stop:1 #2f855a);
                        font-size: 10px; font-weight: bold;
                        border: none; border-radius: 6px; 
                        color: white; padding: 5px;
                    }
                    QPushButton:hover { 
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #48bb78, stop:1 #38a169);
                    }
                """)
            else:
                btn.setFixedSize(120, 40)
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #4299e1, stop:1 #3182ce);
                        font-size: 11px; font-weight: bold;
                        border: none; border-radius: 6px; 
                        color: white; padding: 5px;
                    }
                    QPushButton:hover { 
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #63b3ed, stop:1 #4299e1);
                    }
                """)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
            
        return widget
        
    def create_button_column(self, buttons):
        """Create button column"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)
        widget.setLayout(layout)
        
        for text, callback in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(150, 35)
            
            if "Detect" in text:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #ed8936, stop:1 #dd6b20);
                        font-size: 10px; font-weight: bold;
                        border: none; border-radius: 6px; 
                        color: white; padding: 5px;
                    }
                    QPushButton:hover { 
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #f6ad55, stop:1 #ed8936);
                    }
                """)
            elif text == "Exit":
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #e53e3e, stop:1 #c53030);
                        font-size: 10px; font-weight: bold;
                        border: none; border-radius: 6px; 
                        color: white; padding: 5px;
                    }
                    QPushButton:hover { 
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #fc8181, stop:1 #e53e3e);
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #4299e1, stop:1 #3182ce);
                        font-size: 10px; font-weight: bold;
                        border: none; border-radius: 6px; 
                        color: white; padding: 5px;
                    }
                    QPushButton:hover { 
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #63b3ed, stop:1 #4299e1);
                    }
                """)
            
            btn.clicked.connect(callback)
            layout.addWidget(btn)
            
        return widget
        
    def create_param_bar(self, params):
        """Create enhanced parameter bar"""
        widget = QWidget()
        widget.setFixedHeight(35)
        widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a365d, stop:1 #2c5282);
                border: 1px solid #4a90e2; border-radius: 6px;
            }
        """)
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        widget.setLayout(layout)
        
        for label_text, attr_name in params:
            label = QLabel(label_text)
            label.setStyleSheet("""
                color: #e2e8f0; font-size: 9px; 
                font-weight: bold; background: transparent;
            """)
            layout.addWidget(label)
            
            value_label = QLabel("")
            value_label.setFixedWidth(70)
            value_label.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a5568, stop:1 #2d3748);
                border: 1px solid #4a90e2; border-radius: 3px;
                padding: 2px 4px; color: #e2e8f0; font-size: 8px;
            """)
            setattr(self, attr_name, value_label)
            layout.addWidget(value_label)
            
        layout.addStretch()
        return widget
        
    def display_image(self, image_path, label):
        """Display image with proper scaling"""
        try:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                raise Exception("Invalid image")
                
            label_size = label.size()
            target_size = QSize(label_size.width() - 20, label_size.height() - 20)
            
            scaled_pixmap = pixmap.scaled(
                target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            
            label.setPixmap(scaled_pixmap)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                QLabel {
                    background: transparent;
                    border: 2px solid #4a90e2;
                    border-radius: 8px; padding: 10px;
                }
            """)
            
        except Exception as e:
            label.setText(f"Error: {str(e)}")
            label.setPixmap(QPixmap())
            QMessageBox.critical(self, "Error", f"Failed to display image: {str(e)}")
    
    def browse_input_image(self):
        """Browse input image with DWT analysis"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Input Image", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if filename:
            self.input_image_path = filename
            self.display_image(filename, self.input_image_label)
            # Auto-show DWT analysis
            self.show_original_dwt()
            
    def browse_stego_image(self):
        """Browse stego image with auto-analysis"""
        default_dir = ""
        if os.path.exists("stego_images"):
            default_dir = "stego_images"
        
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Stego Image", default_dir,
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if filename:
            self.stego_image_path = filename
            self.display_image(filename, self.stego_image_label)
            # Auto-show DWT analysis
            self.show_stego_dwt()
            self.check_metadata(filename)
    
    def embed_text(self):
        """Enhanced DWT embedding with comprehensive metrics"""
        if not self.input_image_path:
            QMessageBox.warning(self, "Warning", "Please select an input image first!")
            return
            
        secret_text = self.secret_text.toPlainText()
        if not secret_text:
            QMessageBox.warning(self, "Warning", "Please enter text to hide!")
            return
            
        try:
            self.stego_image_array, metrics = self.dwt.embed_text(
                self.input_image_path, secret_text
            )
            
            # Enhanced filename with DWT info
            original_name = os.path.splitext(os.path.basename(self.input_image_path))[0]
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            text_hash = hashlib.md5(secret_text.encode('utf-8')).hexdigest()[:6]
            output_filename = f"dwt_stego_{original_name}_{timestamp}_{text_hash}.png"
            
            output_dir = "stego_images"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            output_path = os.path.join(output_dir, output_filename)
            
            if self.dwt.save_stego_image(self.stego_image_array, output_path):
                # Enhanced metadata with DWT specifics
                self.save_dwt_metadata(output_dir, original_name, timestamp, 
                                     secret_text, metrics, output_path)
                
                self.display_image(output_path, self.embedded_image_label)
                
                # Update enhanced metrics
                self.embed_time_label.setText(f"{metrics['embedding_time']:.3f}s")
                self.embed_psnr_label.setText(f"{metrics['psnr']:.1f}dB")
                self.ssim_embed_label.setText(f"{metrics['ssim']:.3f}")
                self.capacity_label.setText(f"{metrics['capacity_usage']:.1f}%")
                self.wavelet_label.setText(metrics['wavelet'].upper())
                
                # Auto-set for comparison
                self.stego_image_path = output_path
                
                # Auto-compare DWT
                self.compare_dwt_analysis()
                
                QMessageBox.information(self, "DWT Embedding Success", 
                    f"Text embedded using True DWT Steganography!\n\n"
                    f"File: {output_filename}\n"
                    f"Method: 2-Level {metrics['wavelet'].upper()} DWT\n"
                    f"Channel: {metrics['embedding_channel']}\n"
                    f"PSNR: {metrics['psnr']:.2f} dB\n"
                    f"SSIM: {metrics['ssim']:.4f}\n"
                    f"Capacity Used: {metrics['capacity_usage']:.1f}%\n"
                    f"Bits Embedded: {metrics['bits_embedded']}")
            else:
                QMessageBox.critical(self, "Error", "Failed to save stego image!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"DWT Embedding failed: {str(e)}")
    
    def detect_steganography(self):
        """Enhanced DWT detection"""
        if not self.stego_image_path:
            QMessageBox.warning(self, "Warning", "Please select a stego image first!")
            return
        
        try:
            analysis_result = self.dwt.analyze_image(self.stego_image_path)
            
            is_suspicious = analysis_result['is_suspicious']
            confidence = analysis_result['confidence']
            details = analysis_result['details']
            extracted_text = analysis_result.get('extracted_text')
            
            # Update GUI with enhanced info
            self.detection_label.setText("POSITIVE" if is_suspicious else "NEGATIVE")
            self.confidence_label.setText(f"{confidence:.0f}%")
            self.method_label.setText("DWT-Based")
            
            if is_suspicious:
                self.detection_label.setStyleSheet("""
                    background: #e53e3e; color: white; 
                    border-radius: 3px; padding: 2px 4px; font-size: 8px; font-weight: bold;
                """)
            else:
                self.detection_label.setStyleSheet("""
                    background: #38a169; color: white; 
                    border-radius: 3px; padding: 2px 4px; font-size: 8px; font-weight: bold;
                """)
            
            # Show comprehensive results
            status = "POSITIVE" if is_suspicious else "NEGATIVE"
            message = f"True DWT Steganography Detection: {status}\n"
            message += f"Confidence: {confidence}%\n"
            message += f"Analysis Method: {analysis_result['analysis_method']}\n\n"
            
            if details:
                message += "DWT Detection Results:\n"
                for detail in details:
                    message += f"• {detail}\n"
            
            if extracted_text:
                message += f"\n✓ DWT Extraction SUCCESS: '{extracted_text}'"
                self.extracted_text.setPlainText(extracted_text)
            
            # Auto-show DWT analysis
            self.show_stego_dwt()
            
            self.show_detection_results(status, message)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"DWT Detection failed: {str(e)}")
    
    def extract_text(self):
        """Enhanced DWT extraction"""
        if not self.stego_image_path:
            QMessageBox.warning(self, "Warning", "Please select a stego image first!")
            return
            
        try:
            extracted_text, extraction_time = self.dwt.extract_text(self.stego_image_path)
            
            self.extracted_text.setPlainText(extracted_text)
            self.extract_time_label.setText(f"{extraction_time:.3f}s")
            
            if not extracted_text.startswith("Error"):
                QMessageBox.information(self, "DWT Extraction Success", 
                    f"Text extracted using True DWT method!\n\n"
                    f"Extracted: '{extracted_text}'\n"
                    f"Method: 2-Level DWT Coefficient Analysis\n"
                    f"Time: {extraction_time:.3f} seconds")
            else:
                QMessageBox.warning(self, "DWT Extraction Issue", 
                    f"DWT extraction encountered an issue:\n\n{extracted_text}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"DWT Extraction failed: {str(e)}")
    
    def save_dwt_metadata(self, output_dir, original_name, timestamp, secret_text, metrics, output_path):
        """Save enhanced DWT metadata"""
        try:
            metadata_file = os.path.join(output_dir, f"dwt_metadata_{original_name}_{timestamp}.txt")
            with open(metadata_file, 'w', encoding='utf-8') as f:
                f.write(f"TRUE DWT STEGANOGRAPHY METADATA\n")
                f.write(f"=" * 40 + "\n")
                f.write(f"Algorithm: True DWT Steganography\n")
                f.write(f"Wavelet: {metrics['wavelet']}\n")
                f.write(f"Decomposition Level: 2\n")
                f.write(f"Embedding Location: Mid-frequency coefficients (cH2)\n")
                f.write(f"Embedding Channel: {metrics['embedding_channel']}\n")
                f.write(f"Embedding Method: Quantization-based\n")
                f.write(f"Embedding Strength: {metrics['embedding_strength']}\n")
                f.write(f"\nFILES:\n")
                f.write(f"Original Image: {self.input_image_path}\n")
                f.write(f"Stego Image: {output_path}\n")
                f.write(f"\nMESSAGE INFO:\n")
                f.write(f"Secret Text: {secret_text}\n")
                f.write(f"Text Length: {metrics['text_length']} bytes\n")
                f.write(f"Bits Embedded: {metrics['bits_embedded']}\n")
                f.write(f"Capacity: {metrics['capacity']} coefficients\n")
                f.write(f"Capacity Usage: {metrics['capacity_usage']:.2f}%\n")
                f.write(f"\nQUALITY METRICS:\n")
                f.write(f"Embedding Time: {metrics['embedding_time']:.4f}s\n")
                f.write(f"PSNR: {metrics['psnr']:.2f} dB\n")
                f.write(f"SSIM: {metrics['ssim']:.4f}\n")
                f.write(f"MSE: {metrics['mse']:.3f}\n")
                f.write(f"SNR: {metrics['snr']:.2f} dB\n")
                f.write(f"\nTIMESTAMP:\n")
                f.write(f"Created: {datetime.datetime.now()}\n")
        except Exception as e:
            print(f"DWT metadata save error: {e}")
    
    def check_metadata(self, image_path):
        """Check for DWT metadata"""
        try:
            filename = os.path.basename(image_path)
            if filename.startswith("dwt_stego_"):
                base_name = filename.replace("dwt_stego_", "").replace(".png", "")
                metadata_file = os.path.join(os.path.dirname(image_path), f"dwt_metadata_{base_name}.txt")
                
                if os.path.exists(metadata_file):
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata_content = f.read()
                    
                    QMessageBox.information(self, "DWT Metadata Found", 
                        f"Found DWT steganography metadata:\n\n{metadata_content}")
        except:
            pass
    
    def show_detection_results(self, status, message):
        """Enhanced detection results dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("DWT Steganography Detection Results")
        dialog.setFixedSize(700, 500)
        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d3748, stop:1 #1a202c);
                color: #e2e8f0;
            }
        """)
        
        layout = QVBoxLayout()
        
        status_label = QLabel(f"DWT Detection: {status}")
        status_label.setAlignment(Qt.AlignCenter)
        if status == "POSITIVE":
            status_label.setStyleSheet("""
                font-size: 16px; font-weight: bold; color: white; 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e53e3e, stop:1 #c53030);
                padding: 15px; border-radius: 8px; margin: 10px;
            """)
        else:
            status_label.setStyleSheet("""
                font-size: 16px; font-weight: bold; color: white; 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #38a169, stop:1 #2f855a);
                padding: 15px; border-radius: 8px; margin: 10px;
            """)
        layout.addWidget(status_label)
        
        text_area = QTextEdit()
        text_area.setPlainText(message)
        text_area.setReadOnly(True)
        text_area.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a5568, stop:1 #2d3748);
                border: 2px solid #4a90e2; border-radius: 8px;
                font-family: 'Courier New'; font-size: 11px;
                padding: 10px; color: #e2e8f0;
            }
        """)
        layout.addWidget(text_area)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4299e1, stop:1 #3182ce);
                color: white; border: none; padding: 8px 16px;
                border-radius: 4px; font-weight: bold;
            }
        """)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def open_stego_folder(self):
        """Open stego folder"""
        if not os.path.exists("stego_images"):
            os.makedirs("stego_images")
            
        try:
            if sys.platform == "darwin":
                os.system(f"open stego_images")
            elif sys.platform == "win32":
                os.system(f"explorer stego_images")
            else:
                os.system(f"xdg-open stego_images")
        except:
            QMessageBox.information(self, "Folder Location", 
                f"DWT stego images location:\n{os.path.abspath('stego_images')}")
            
    def reset_all(self):
        """Enhanced reset with DWT cleanup"""
        self.input_image_path = None
        self.stego_image_path = None
        self.stego_image_array = None
        
        # Clear all images
        for label in [self.input_image_label, self.embedded_image_label, self.stego_image_label]:
            label.clear()
            label.setText("No Image")
        
        # Clear text areas
        self.secret_text.setPlainText("Hello DWT Steganography! 🔐")
        self.extracted_text.clear()
        self.dwt_analysis.clear()
        
        # Clear all metrics
        for attr in ['embed_time_label', 'embed_psnr_label', 'ssim_embed_label', 
                     'capacity_label', 'wavelet_label', 'extract_time_label', 
                     'detection_label', 'confidence_label', 'method_label']:
            getattr(self, attr).clear()
        
        # Clear DWT visualization
        self.dwt_widget.figure.clear()
        self.dwt_widget.canvas.draw()
        
        QMessageBox.information(self, "Reset Complete", 
            "All DWT analysis data cleared!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMessageBox {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2d3748, stop:1 #1a202c);
            color: #e2e8f0;
        }
        QMessageBox QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4299e1, stop:1 #3182ce);
            color: white; border: none;
            padding: 8px 16px; border-radius: 4px;
            font-weight: bold; min-width: 80px;
        }
        QFileDialog {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2d3748, stop:1 #1a202c);
            color: #e2e8f0;
        }
    """)
    
    window = DWTSteganographyGUI()
    window.show()
    sys.exit(app.exec_())