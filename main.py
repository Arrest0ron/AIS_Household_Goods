import sys
import os
import logging
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"ais_{datetime.now():%Y%m%d_%H%M%S}.log")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("main")

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from ui.login_window import LoginWindow
from ui.styles import PURPLE_STYLESHEET


def main():
    log.info("=== Приложение запущено ===")
    try:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        app.setStyleSheet(PURPLE_STYLESHEET)
        font = QFont("Segoe UI", 10)
        app.setFont(font)
        window = LoginWindow()
        window.show()
        log.info("Окно входа отображено")
        sys.exit(app.exec())
    except Exception:
        log.exception("Фатальное исключение в main()")
        raise


if __name__ == "__main__":
    main()
