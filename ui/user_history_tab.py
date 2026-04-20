from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLineEdit,
    QTableWidget, QTableWidgetItem, QSplitter, QLabel, QMessageBox,
    QFileDialog, QDateEdit
)
from PyQt6.QtCore import Qt, QDate, QEvent
from repositories.order_repository import OrderRepository
from repositories.customer_repository import CustomerRepository
from services.pdf_reports import ReportService
from session import Session


class UserHistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.order_repo = OrderRepository()
        self.customer_repo = CustomerRepository()

        self.customer_combo = QComboBox()
        self.customer_label = QLabel()
        self.refresh_btn = QPushButton("Обновить")
        self.contract_btn = QPushButton("Договор")

        user = Session.current_user or {}
        self._customer_id = user.get("customer_id")

        if self._customer_id:
            self.customer_combo.hide()
            self.customer_label.show()
            try:
                cust = self.customer_repo.get_by_id(self._customer_id)
                self.customer_label.setText(cust.get("customer_name", "") if cust else "")
            except Exception:
                self.customer_label.setText(f"ID: {self._customer_id}")
            self.load_orders()
        else:
            self.customer_label.hide()
            self.customer_combo.currentIndexChanged.connect(self.load_orders)
            self.refresh_customers()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по описанию")
        self.search_btn = QPushButton("Найти")
        self.search_btn.clicked.connect(self.search)

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate(2020, 1, 1))
        self.date_from.setDisplayFormat("yyyy-MM-dd")
        self.date_from.dateChanged.connect(self.search)

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setDisplayFormat("yyyy-MM-dd")
        self.date_to.dateChanged.connect(self.search)

        self.reset_dates_btn = QPushButton("Сброс")
        self.reset_dates_btn.clicked.connect(self.reset_dates)

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(["№", "Дата", "Описание", "Скидка", "Сумма (₽)"])
        self.order_table.setSortingEnabled(True)
        self.order_table.itemSelectionChanged.connect(self.load_items)

        self.item_table = QTableWidget()
        self.item_table.setColumnCount(3)
        self.item_table.setHorizontalHeaderLabels(["Товар", "Цена (₽)", "Количество"])
        self.item_table.setSortingEnabled(True)

        top = QHBoxLayout()
        top.addWidget(QLabel("Покупатель:"))
        top.addWidget(self.customer_combo, 1)
        top.addWidget(self.customer_label, 1)
        top.addWidget(self.search_input)
        top.addWidget(self.search_btn)
        top.addWidget(QLabel("С:"))
        top.addWidget(self.date_from)
        top.addWidget(QLabel("По:"))
        top.addWidget(self.date_to)
        top.addWidget(self.reset_dates_btn)
        top.addWidget(self.refresh_btn)
        top.addWidget(self.contract_btn)

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
        self.contract_btn.clicked.connect(self.export_contract)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_orders()

    def refresh_customers(self):
        self.customer_combo.blockSignals(True)
        self.customer_combo.clear()
        customers = self.customer_repo.get_all()
        for c in customers:
            self.customer_combo.addItem(f'{c["customer_name"]} ({c.get("phone", "—")})', c["customer_id"])
        self.customer_combo.blockSignals(False)
        self.load_orders()

    def load_orders(self):
        customer_id = self._customer_id or self.customer_combo.currentData()
        if not customer_id:
            self.order_table.setRowCount(0)
            return
        rows = self.order_repo.get_all()
        filtered = [r for r in rows if r["customer_id"] == customer_id]
        text = self.search_input.text().strip()
        if text:
            filtered = [r for r in filtered if text.lower() in (r.get("description") or "").lower()]
        start = self.date_from.date().toString("yyyy-MM-dd")
        end = self.date_to.date().toString("yyyy-MM-dd")
        filtered = [r for r in filtered if start <= str(r.get("order_date", "")) <= end]
        self._fill_orders(filtered)

    def search(self):
        self.load_orders()

    def reset_dates(self):
        self.date_from.setDate(QDate(2020, 1, 1))
        self.date_to.setDate(QDate.currentDate())

    def _fill_orders(self, filtered):
        self.order_table.setRowCount(len(filtered))
        for i, r in enumerate(filtered):
            self.order_table.setItem(i, 0, QTableWidgetItem(str(r["order_id"])))
            self.order_table.setItem(i, 1, QTableWidgetItem(str(r.get("order_date", ""))))
            desc = r.get("description", "") or ""
            self.order_table.setItem(i, 2, QTableWidgetItem(desc[:60] + "..." if len(desc) > 60 else desc))
            self.order_table.setItem(i, 3, QTableWidgetItem(f'{float(r.get("discount", 0)):.2f}%'))
            items = self.order_repo.get_items(r["order_id"])
            total = sum(float(it.get("price", 0)) * it.get("amount", 0) for it in items)
            discount = float(r.get("discount", 0))
            total = total * (1 - discount / 100)
            self.order_table.setItem(i, 4, QTableWidgetItem(f'{total:.2f}'))
        self.order_table.resizeColumnsToContents()
        self.load_items()

    def export_contract(self):
        row = self.order_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ")
            return
        order_id_item = self.order_table.item(row, 0)
        if not order_id_item:
            return
        order_id = int(order_id_item.text())
        path, _ = QFileDialog.getSaveFileName(
            self, "Договор купли-продажи",
            f"Договор_купли_продажи_{order_id}.pdf", "PDF Files (*.pdf)")
        if not path:
            return
        try:
            ReportService().purchase_contract(path, order_id)
            import os; os.startfile(path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать договор:\n{e}")

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
