from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QTabWidget
from session import Session
from ui.categories_tab import CategoriesTab
from ui.warehouses_tab import WarehousesTab
from ui.suppliers_tab import SuppliersTab
from ui.items_tab import ItemsTab
from ui.customers_tab import CustomersTab
from ui.supplies_tab import SuppliesTab
from ui.orders_tab import OrdersTab
from ui.reports_tab import ReportsTab


class AdminMainWindow(QMainWindow):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("AIS_Shop — Администратор")
        self.resize(1400, 800)

        central = QWidget()
        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.addTab(CategoriesTab(), "Категории")
        self.tabs.addTab(WarehousesTab(), "Склады")
        self.tabs.addTab(SuppliersTab(), "Поставщики")
        self.tabs.addTab(ItemsTab(), "Товары")
        self.tabs.addTab(CustomersTab(), "Покупатели")
        self.tabs.addTab(SuppliesTab(), "Поставки")
        self.tabs.addTab(OrdersTab(), "Заказы")
        self.tabs.addTab(ReportsTab(), "Отчёты")

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
