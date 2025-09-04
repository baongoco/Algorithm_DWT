# dwt_gui_simple.py - Test version
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DWTSteganographyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("DWT Based Image Steganography - Test")
        self.setFixedSize(800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Add title
        title = QLabel("DWT Steganography Test")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Add test button
        test_btn = QPushButton("Test Button")
        test_btn.setFixedSize(200, 50)
        test_btn.clicked.connect(self.test_function)
        layout.addWidget(test_btn, alignment=Qt.AlignCenter)
        
        # Add label
        self.status_label = QLabel("GUI is working!")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; color: green; margin: 20px;")
        layout.addWidget(self.status_label)
        
    def test_function(self):
        QMessageBox.information(self, "Test", "Button clicked! GUI is working properly.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DWTSteganographyGUI()
    window.show()
    sys.exit(app.exec_())