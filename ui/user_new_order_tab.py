from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton,
    QComboBox, QTextEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QSpinBox, QDialog
)
from repositories.order_repository import OrderRepository
from repositories.customer_repository import CustomerRepository
from repositories.item_repository import ItemRepository
from datetime import date


class SelectItemDialog(QDialog):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор товара")
        self.resize(500, 400)
        self.selected_items = []

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Название", "Цена (₽)", "Остаток", "Кол-во"])
        self.table.setRowCount(len(items))
        self._items = items

        for i, item in enumerate(items):
            self.table.setItem(i, 0, QTableWidgetItem(item["item_name"]))
            self.table.setItem(i, 1, QTableWidgetItem(f'{float(item["price"]):.2f}'))
            self.table.setItem(i, 2, QTableWidgetItem(str(item["stock_quantity"])))
            spin = QSpinBox()
            spin.setRange(0, item["stock_quantity"])
            self.table.setCellWidget(i, 3, spin)

        btn_ok = QPushButton("Добавить выбранное")
        btn_ok.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(btn_ok)
        self.setLayout(layout)

    def get_selected(self):
        result = []
        for i, item in enumerate(self._items):
            spin = self.table.cellWidget(i, 3)
            qty = spin.value()
            if qty > 0:
                result.append({"item_id": item["item_id"], "item_name": item["item_name"],
                               "price": float(item["price"]), "amount": qty})
        return result


class UserNewOrderTab(QWidget):
    def __init__(self):
        super().__init__()
        self.order_repo = OrderRepository()
        self.customer_repo = CustomerRepository()
        self.item_repo = ItemRepository()
        self.order_items = []

        # Customer selection
        self.customer_combo = QComboBox()
        self.refresh_customers()

        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(60)

        self.add_items_btn = QPushButton("Выбрать товары")
        self.clear_btn = QPushButton("Очистить")
        self.submit_btn = QPushButton("Оформить заказ")

        self.items_table = QTableWidget()
        self.items_table.setColumnCount(4)
        self.items_table.setHorizontalHeaderLabels(["Товар", "Цена (₽)", "Кол-во", "Сумма (₽)"])
        self.items_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        form = QFormLayout()
        form.addRow("Покупатель:", self.customer_combo)
        form.addRow("Описание:", self.desc_edit)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.add_items_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.clear_btn)
        btn_row.addWidget(self.submit_btn)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(btn_row)
        layout.addWidget(self.items_table)
        self.setLayout(layout)

        self.add_items_btn.clicked.connect(self.add_items)
        self.clear_btn.clicked.connect(self.clear_items)
        self.submit_btn.clicked.connect(self.submit_order)

    def refresh_customers(self):
        self.customer_combo.clear()
        customers = self.customer_repo.get_all()
        for c in customers:
            self.customer_combo.addItem(f'{c["customer_name"]} ({c.get("phone", "—")})', c["customer_id"])

    def refresh_items_table(self):
        self.items_table.setRowCount(len(self.order_items))
        total = 0
        for i, item in enumerate(self.order_items):
            self.items_table.setItem(i, 0, QTableWidgetItem(item["item_name"]))
            self.items_table.setItem(i, 1, QTableWidgetItem(f'{item["price"]:.2f}'))
            self.items_table.setItem(i, 2, QTableWidgetItem(str(item["amount"])))
            line_total = item["price"] * item["amount"]
            self.items_table.setItem(i, 3, QTableWidgetItem(f'{line_total:.2f}'))
            total += line_total
        self.items_table.resizeColumnsToContents()

    def add_items(self):
        items = self.item_repo.get_all()
        dialog = SelectItemDialog(items, self)
        if dialog.exec_():
            selected = dialog.get_selected()
            for s in selected:
                existing = next((x for x in self.order_items if x["item_id"] == s["item_id"]), None)
                if existing:
                    existing["amount"] += s["amount"]
                else:
                    self.order_items.append(s)
            self.refresh_items_table()

    def clear_items(self):
        self.order_items.clear()
        self.refresh_items_table()

    def submit_order(self):
        customer_id = self.customer_combo.currentData()
        if customer_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите покупателя")
            return
        if not self.order_items:
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы один товар")
            return

        try:
            data = {
                "customer_id": customer_id,
                "description": self.desc_edit.toPlainText().strip(),
                "delivery_needed": False,
                "delivery_time": None,
                "discount": 0
            }
            result = self.order_repo.create(data)
            order_id = result["order_id"] if isinstance(result, dict) else result[0]
            for item in self.order_items:
                self.order_repo.add_item(order_id, item["item_id"], item["amount"])
            QMessageBox.information(self, "Успех", f"Заказ №{order_id} оформлен")
            self.clear_items()
            self.desc_edit.clear()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось оформить заказ:\n{e}")
