# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication
from dwt_gui import DWTSteganographyGUI

def main():
    """Main function to run the DWT Steganography application"""
    
    # Create QApplication instance
    app = QApplication(sys.argv)
    
    # Set application style for better appearance on macOS
    app.setStyle('Fusion')
    
    # Create and show main window
    window = DWTSteganographyGUI()
    window.show()
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()