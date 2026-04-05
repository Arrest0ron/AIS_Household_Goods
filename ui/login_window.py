from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QMessageBox, QLabel, QHBoxLayout
)
from services.auth_service import AuthService
from session import Session
from ui.admin_main_window import AdminMainWindow
from ui.user_main_window import UserMainWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()
        self.setWindowTitle("Вход в систему — AIS_Shop")
        self.resize(400, 200)

        title = QLabel("Информационная система магазина")
        title.setStyleSheet("font-size: 16pt; font-weight: bold;")

        self.login_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Вход")
        self.exit_btn = QPushButton("Выход")

        form = QFormLayout()
        form.addRow("Логин:", self.login_edit)
        form.addRow("Пароль:", self.password_edit)

        buttons = QHBoxLayout()
        buttons.addWidget(self.login_btn)
        buttons.addWidget(self.exit_btn)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addLayout(buttons)
        self.setLayout(layout)

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
