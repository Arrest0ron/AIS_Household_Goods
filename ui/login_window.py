from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QMessageBox, QLabel, QFrame
)
from PyQt6.QtCore import Qt
from services.auth_service import AuthService
from session import Session
from ui.admin_main_window import AdminMainWindow
from ui.user_main_window import UserMainWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()
        self.setWindowTitle("AIS_Shop — Вход в систему")
        self.resize(480, 360)
        self.setMinimumSize(480, 360)

        # Background
        self.setStyleSheet("""
            LoginWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #F3EEFF, stop:1 #E8DFF5);
            }
        """)

        # Card
        card = QFrame()
        card.setObjectName("loginCard")
        card.setStyleSheet("""
            #loginCard {
                background: #FFFFFF;
                border: 1px solid #D8CCF0;
                border-radius: 16px;
                padding: 30px;
            }
        """)
        card_layout = QVBoxLayout()
        card_layout.setSpacing(16)

        icon_label = QLabel("🏪")
        icon_label.setStyleSheet("font-size: 36px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Информационная система\nмагазина")
        title.setStyleSheet("font-size: 18pt; font-weight: 700; color: #4A2D8A;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Введите учётные данные для входа")
        subtitle.setStyleSheet("font-size: 10pt; color: #7C6F9A;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.login_edit = QLineEdit()
        self.login_edit.setPlaceholderText("Логин")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Пароль")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Войти")
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7C3AED, stop:1 #A78BFA);
                color: #fff; border: none; padding: 12px; border-radius: 8px;
                font-size: 12pt; font-weight: 700;
            }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #6D28D9, stop:1 #8B5CF6); }
        """)

        self.exit_btn = QPushButton("Отмена")
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background: transparent; color: #7C6F9A; border: 2px solid #D8CCF0;
                padding: 10px; border-radius: 8px; font-size: 10pt;
            }
            QPushButton:hover { background: #F3EEFF; border-color: #A78BFA; color: #6D28D9; }
        """)

        card_layout.addWidget(icon_label)
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(8)
        card_layout.addWidget(self.login_edit)
        card_layout.addWidget(self.password_edit)
        card_layout.addSpacing(8)
        card_layout.addWidget(self.login_btn)
        card_layout.addWidget(self.exit_btn)

        card.setLayout(card_layout)

        # Center card in window
        outer = QVBoxLayout()
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(card, 0, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(outer)

        self.login_btn.clicked.connect(self.handle_login)
        self.exit_btn.clicked.connect(self.close)

        self.child_window = None

    def handle_login(self):
        login = self.login_edit.text().strip()
        password = self.password_edit.text().strip()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        user, error = self.auth_service.login(login, password)
        if error:
            QMessageBox.warning(self, "Ошибка входа", error)
            return

        Session.login(user)
        self.hide()

        if Session.is_admin():
            self.child_window = AdminMainWindow(self)
        else:
            self.child_window = UserMainWindow(self)

        self.child_window.show()

    def return_back(self):
        self.login_edit.clear()
        self.password_edit.clear()
        self.show()
