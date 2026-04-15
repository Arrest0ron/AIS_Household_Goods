from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout,
    QComboBox, QSpinBox, QFileDialog
)
from PyQt6.QtCore import Qt
from repositories.order_repository import OrderRepository
from ui.dialogs import OrderDialog
from services.pdf_reports import ReportService


class OrderItemDialog(QDialog):
    def __init__(self, parent=None, items=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Позиция заказа")
        self.resize(400, 120)

        self.item_combo = QComboBox()
        self._items = items or []
        for it in self._items:
            self.item_combo.addItem(f'{it["item_name"]} ({it["price"]:.2f} ₽)', it["item_id"])
        self.amount_spin = QSpinBox()
        self.amount_spin.setRange(1, 999999)

        form = QFormLayout()
        form.addRow("Товар:", self.item_combo)
        form.addRow("Количество:", self.amount_spin)

        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Отмена")
        btn_cancel.clicked.connect(self.reject)

        buttons = QHBoxLayout()
        buttons.addWidget(btn_ok)
        buttons.addWidget(btn_cancel)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(buttons)
        self.setLayout(layout)

        if data:
            idx = self.item_combo.findData(data["item_id"])
            if idx >= 0:
                self.item_combo.setCurrentIndex(idx)
            self.amount_spin.setValue(data["amount"])

    def get_data(self):
        return {
            "item_id": self.item_combo.currentData(),
            "amount": self.amount_spin.value()
        }


class OrdersTab(QWidget):
    def __init__(self):
        super().__init__()
        self.repo = OrderRepository()
        self.current_ids = []
        self.current_item_ids = []

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(6)
        self.order_table.setHorizontalHeaderLabels(["Покупатель", "Дата", "Доставка", "Скидка", "Описание", "ID"])
        self.order_table.setColumnHidden(5, True)
        self.order_table.itemSelectionChanged.connect(self.on_order_selected)

        order_buttons = QHBoxLayout()
        self.add_order_btn = QPushButton("+ Заказ")
        self.edit_order_btn = QPushButton("Изменить")
        self.delete_order_btn = QPushButton("Удалить")
        self.pdf_order_btn = QPushButton("PDF")
        order_buttons.addWidget(self.add_order_btn)
        order_buttons.addWidget(self.edit_order_btn)
        order_buttons.addWidget(self.delete_order_btn)
        order_buttons.addStretch()
        order_buttons.addWidget(self.pdf_order_btn)

        self.item_table = QTableWidget()
        self.item_table.setColumnCount(4)
        self.item_table.setHorizontalHeaderLabels(["Товар", "Цена", "Количество", "ID"])
        self.item_table.setColumnHidden(3, True)

        item_buttons = QHBoxLayout()
        self.add_item_btn = QPushButton("+ Товар")
        self.edit_item_btn = QPushButton("Изменить")
        self.delete_item_btn = QPushButton("Удалить")
        item_buttons.addWidget(self.add_item_btn)
        item_buttons.addWidget(self.edit_item_btn)
        item_buttons.addWidget(self.delete_item_btn)
        item_buttons.addStretch()

        top_widget = QWidget()
        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self.order_table)
        top_layout.addLayout(order_buttons)
        top_widget.setLayout(top_layout)

        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(self.item_table)
        bottom_layout.addLayout(item_buttons)
        bottom_widget.setLayout(bottom_layout)

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(top_widget)
        splitter.addWidget(bottom_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        self.add_order_btn.clicked.connect(self.add_order)
        self.edit_order_btn.clicked.connect(self.edit_order)
        self.delete_order_btn.clicked.connect(self.delete_order)
        self.pdf_order_btn.clicked.connect(self.export_pdf)
        self.add_item_btn.clicked.connect(self.add_item)
        self.edit_item_btn.clicked.connect(self.edit_item)
        self.delete_item_btn.clicked.connect(self.delete_item)

        self.load_data()

    def get_selected_order_id(self):
        row = self.order_table.currentRow()
        if row < 0 or row >= len(self.current_ids):
            return None
        return self.current_ids[row]

    def get_selected_item_id(self):
        row = self.item_table.currentRow()
        if row < 0 or row >= len(self.current_item_ids):
            return None
        return self.current_item_ids[row]

    def load_data(self):
        rows = self.repo.get_all()
        self.current_ids = [r["order_id"] for r in rows]
        self.order_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.order_table.setItem(i, 0, QTableWidgetItem(row.get("customer_name", "—")))
            d = row.get("order_date")
            self.order_table.setItem(i, 1, QTableWidgetItem(str(d) if d else "—"))
            self.order_table.setItem(i, 2, QTableWidgetItem("Да" if row.get("delivery_needed") else "Нет"))
            self.order_table.setItem(i, 3, QTableWidgetItem(f'{row.get("discount", 0):.2f}%'))
            desc = row.get("description") or ""
            self.order_table.setItem(i, 4, QTableWidgetItem(desc[:50] + "..." if len(desc) > 50 else desc))
            self.order_table.setItem(i, 5, QTableWidgetItem(str(row["order_id"])))
        self.order_table.resizeColumnsToContents()
        self.load_items()

    def load_items(self):
        order_id = self.get_selected_order_id()
        if not order_id:
            self.item_table.setRowCount(0)
            self.current_item_ids = []
            return
        rows = self.repo.get_items(order_id)
        self.current_item_ids = [r["position_id"] for r in rows]
        self.item_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.item_table.setItem(i, 0, QTableWidgetItem(row.get("item_name", "—")))
            self.item_table.setItem(i, 1, QTableWidgetItem(f'{row.get("price", 0):.2f}'))
            self.item_table.setItem(i, 2, QTableWidgetItem(str(row.get("amount", 0))))
            self.item_table.setItem(i, 3, QTableWidgetItem(str(row["position_id"])))
        self.item_table.resizeColumnsToContents()

    def on_order_selected(self):
        self.load_items()

    def add_order(self):
        customers = self.repo.get_all_customers()
        dialog = OrderDialog(self, customers=customers)
        if dialog.exec_():
            self.repo.create(dialog.get_data())
            self.load_data()

    def edit_order(self):
        order_id = self.get_selected_order_id()
        if not order_id:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ")
            return
        data = self.repo.get_by_id(order_id)
        customers = self.repo.get_all_customers()
        dialog = OrderDialog(self, data=data, customers=customers)
        if dialog.exec_():
            self.repo.update(order_id, dialog.get_data())
            self.load_data()

    def delete_order(self):
        order_id = self.get_selected_order_id()
        if not order_id:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить заказ?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.repo.delete(order_id)
            self.load_data()

    def add_item(self):
        order_id = self.get_selected_order_id()
        if not order_id:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ")
            return
        items = self.repo.get_all_items()
        dialog = OrderItemDialog(self, items=items)
        if dialog.exec_():
            data = dialog.get_data()
            if data["item_id"] is None:
                QMessageBox.warning(self, "Ошибка", "Выберите товар")
                return
            self.repo.add_item(order_id, data["item_id"], data["amount"])
            self.load_items()

    def edit_item(self):
        position_id = self.get_selected_item_id()
        if not position_id:
            QMessageBox.warning(self, "Ошибка", "Выберите позицию")
            return
        order_id = self.get_selected_order_id()
        items = self.repo.get_all_items()
        data = {"item_id": None, "amount": 0}
        for r in self.repo.get_items(order_id):
            if r["position_id"] == position_id:
                data = r
                break
        dialog = OrderItemDialog(self, items=items, data=data)
        if dialog.exec_():
            d = dialog.get_data()
            self.repo.update_item(position_id, d["amount"])
            self.load_items()

    def delete_item(self):
        position_id = self.get_selected_item_id()
        if not position_id:
            QMessageBox.warning(self, "Ошибка", "Выберите позицию")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить позицию?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.repo.delete_item(position_id)
            self.load_items()

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "PDF — Заказы", "Заказы.pdf", "PDF Files (*.pdf)")
        if not path:
            return
        try:
            ReportService().orders_report(path)
            import os; os.startfile(path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить PDF:\n{e}")
