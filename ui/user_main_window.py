from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QTabWidget
from session import Session
from ui.user_categories_tab import UserCategoriesTab
from ui.user_items_tab import UserItemsTab
from ui.user_new_order_tab import UserNewOrderTab
from ui.user_history_tab import UserHistoryTab


class UserMainWindow(QMainWindow):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("AIS_Shop — Пользователь")
        self.resize(1200, 700)

        central = QWidget()
        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.addTab(UserCategoriesTab(), "Категории")
        self.tabs.addTab(UserItemsTab(), "Товары")
        self.tabs.addTab(UserNewOrderTab(), "Новый заказ")
        self.tabs.addTab(UserHistoryTab(), "Мои заказы")

        self.logout_btn = QPushButton("Выход")
        self.logout_btn.clicked.connect(self.logout)

        layout.addWidget(self.tabs)
        layout.addWidget(self.logout_btn)
        central.setLayout(layout)
        self.setCentralWidget(central)

    def logout(self):
        Session.logout()
        self.close()
        self.login_window.return_back()
