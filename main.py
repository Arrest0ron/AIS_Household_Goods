import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from ui.login_window import LoginWindow
from ui.styles import PURPLE_STYLESHEET


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(PURPLE_STYLESHEET)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
