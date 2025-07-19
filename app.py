import sys

from PySide6.QtWidgets import QApplication

from main_window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())