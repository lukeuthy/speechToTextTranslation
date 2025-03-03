import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import TranslatorApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # For consistent look across platforms
    
    # Set application-wide stylesheet
    app.setStyleSheet("""
        QMainWindow, QDialog {
            background-color: white;
        }
    """)
    print("Updating visualizer...")
    window = TranslatorApp()
    window.show()
    
    sys.exit(app.exec_())