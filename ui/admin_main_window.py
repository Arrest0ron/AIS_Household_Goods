import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget, QLabel
)
from PyQt6.QtCore import Qt
from session import Session
from ui.categories_tab import CategoriesTab
from ui.warehouses_tab import WarehousesTab
from ui.suppliers_tab import SuppliersTab
from ui.items_tab import ItemsTab
from ui.customers_tab import CustomersTab
from ui.supplies_tab import SuppliesTab
from ui.orders_tab import OrdersTab
from ui.reports_tab import ReportsTab
from ui.charts_tab import ChartsTab

log = logging.getLogger("ui.admin")


class AdminMainWindow(QMainWindow):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("AIS_Shop — Администратор")
        self.showMaximized()
        self.setMaximumWidth(1400)

        # Header
        header = QWidget()
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #7C3AED, stop:1 #A78BFA);
            border-radius: 0px;
            padding: 4px;
        """)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(16, 8, 16, 8)

        app_title = QLabel("АИС Магазина бытовых товаров")
        app_title.setStyleSheet("color: #FFFFFF; font-size: 16pt; font-weight: 700; background: transparent;")

        role_badge = QLabel("Администратор")
        role_badge.setStyleSheet("""
            background: rgba(255,255,255,0.2);
            color: #FFFFFF;
            padding: 4px 14px;
            border-radius: 12px;
            font-size: 9pt;
            font-weight: 600;
        """)

        user_name = Session.current_user.get("login", "") if Session.current_user else ""
        user_label = QLabel(user_name)
        user_label.setStyleSheet("color: rgba(255,255,255,0.85); font-size: 10pt; background: transparent;")

        self.logout_btn = QPushButton("Выход")
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.15); color: #FFFFFF;
                border: 1px solid rgba(255,255,255,0.3);
                padding: 6px 16px; border-radius: 6px; font-weight: 600;
            }
            QPushButton:hover { background: rgba(255,255,255,0.25); }
        """)
        self.logout_btn.clicked.connect(self.logout)

        header_layout.addWidget(app_title)
        header_layout.addWidget(role_badge)
        header_layout.addStretch()
        header_layout.addWidget(user_label)
        header_layout.addWidget(self.logout_btn)
        header.setLayout(header_layout)

        # Tabs
        self.tabs = QTabWidget()
        tab_classes = [
            ("Категории", CategoriesTab),
            ("Склады", WarehousesTab),
            ("Поставщики", SuppliersTab),
            ("Товары", ItemsTab),
            ("Покупатели", CustomersTab),
            ("Поставки", SuppliesTab),
            ("Заказы", OrdersTab),
            ("Отчёты", ReportsTab),
            ("Аналитика", ChartsTab),
        ]
        for name, cls in tab_classes:
            try:
                log.info("Инициализация вкладки: %s", name)
                self.tabs.addTab(cls(), name)
            except Exception:
                log.exception("Ошибка при создании вкладки '%s'", name)
                from PyQt6.QtWidgets import QWidget as W
                self.tabs.addTab(W(), name)

        central = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(header)
        layout.addWidget(self.tabs)
        central.setLayout(layout)
        self.setCentralWidget(central)

    def logout(self):
        Session.logout()
        self.close()
        self.login_window.return_back()
