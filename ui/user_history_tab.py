from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox,
    QTableWidget, QTableWidgetItem, QSplitter, QLabel
)
from PyQt6.QtCore import Qt
from repositories.order_repository import OrderRepository
from repositories.customer_repository import CustomerRepository


class UserHistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.order_repo = OrderRepository()
        self.customer_repo = CustomerRepository()

        self.customer_combo = QComboBox()
        self.refresh_btn = QPushButton("Обновить")
        self.customer_combo.currentIndexChanged.connect(self.load_orders)

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(["№", "Дата", "Описание", "Скидка", "Сумма (₽)"])
        self.order_table.itemSelectionChanged.connect(self.load_items)

        self.item_table = QTableWidget()
        self.item_table.setColumnCount(3)
        self.item_table.setHorizontalHeaderLabels(["Товар", "Цена (₽)", "Количество"])

        self.refresh_customers()

        top = QHBoxLayout()
        top.addWidget(QLabel("Покупатель:"))
        top.addWidget(self.customer_combo, 1)
        top.addWidget(self.refresh_btn)

        top_widget = QWidget()
        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self.order_table)
        top_widget.setLayout(top_layout)

        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(QLabel("Состав заказа:"))
        bottom_layout.addWidget(self.item_table)
        bottom_widget.setLayout(bottom_layout)

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(top_widget)
        splitter.addWidget(bottom_widget)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.refresh_btn.clicked.connect(self.refresh_customers)

    def refresh_customers(self):
        self.customer_combo.blockSignals(True)
        self.customer_combo.clear()
        customers = self.customer_repo.get_all()
        for c in customers:
            self.customer_combo.addItem(f'{c["customer_name"]} ({c.get("phone", "—")})', c["customer_id"])
        self.customer_combo.blockSignals(False)
        self.load_orders()

    def load_orders(self):
        customer_id = self.customer_combo.currentData()
        if not customer_id:
            self.order_table.setRowCount(0)
            return
        rows = self.order_repo.get_all()
        filtered = [r for r in rows if r["customer_id"] == customer_id]
        self.order_table.setRowCount(len(filtered))
        for i, r in enumerate(filtered):
            self.order_table.setItem(i, 0, QTableWidgetItem(str(r["order_id"])))
            self.order_table.setItem(i, 1, QTableWidgetItem(str(r.get("order_date", ""))))
            desc = r.get("description", "") or ""
            self.order_table.setItem(i, 2, QTableWidgetItem(desc[:60] + "..." if len(desc) > 60 else desc))
            self.order_table.setItem(i, 3, QTableWidgetItem(f'{float(r.get("discount", 0)):.2f}%'))
        self.order_table.resizeColumnsToContents()
        self.load_items()

    def load_items(self):
        row = self.order_table.currentRow()
        if row < 0:
            self.item_table.setRowCount(0)
            return
        order_id_item = self.order_table.item(row, 0)
        if not order_id_item:
            self.item_table.setRowCount(0)
            return
        order_id = int(order_id_item.text())
        items = self.order_repo.get_items(order_id)
        self.item_table.setRowCount(len(items))
        for i, item in enumerate(items):
            self.item_table.setItem(i, 0, QTableWidgetItem(item.get("item_name", "—")))
            self.item_table.setItem(i, 1, QTableWidgetItem(f'{float(item.get("price", 0)):.2f}'))
            self.item_table.setItem(i, 2, QTableWidgetItem(str(item.get("amount", 0))))
        self.item_table.resizeColumnsToContents()
