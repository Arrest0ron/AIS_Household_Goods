from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout,
    QComboBox, QSpinBox, QFileDialog
)
from PyQt6.QtCore import Qt
from repositories.supply_repository import SupplyRepository
from ui.dialogs import SupplyDialog
from services.pdf_reports import ReportService


class SupplyItemDialog(QDialog):
    def __init__(self, parent=None, items=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Позиция поставки")
        self.resize(400, 120)

        self.item_combo = QComboBox()
        self._items = items or []
        for it in self._items:
            self.item_combo.addItem(f'{it["item_name"]} (ост. {it["stock_quantity"]})', it["item_id"])
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 999999)

        form = QFormLayout()
        form.addRow("Товар:", self.item_combo)
        form.addRow("Количество:", self.quantity_spin)

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
            self.quantity_spin.setValue(data["quantity"])

    def get_data(self):
        return {
            "item_id": self.item_combo.currentData(),
            "quantity": self.quantity_spin.value()
        }


class SuppliesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.repo = SupplyRepository()
        self.current_ids = []
        self.current_item_ids = []

        self.supply_table = QTableWidget()
        self.supply_table.setColumnCount(4)
        self.supply_table.setHorizontalHeaderLabels(["Поставщик", "Склад", "Дата", "ID"])
        self.supply_table.setColumnHidden(3, True)
        self.supply_table.itemSelectionChanged.connect(self.on_supply_selected)

        supply_buttons = QHBoxLayout()
        self.add_supply_btn = QPushButton("+ Поставка")
        self.edit_supply_btn = QPushButton("Изменить")
        self.delete_supply_btn = QPushButton("Удалить")
        self.pdf_supply_btn = QPushButton("PDF")
        supply_buttons.addWidget(self.add_supply_btn)
        supply_buttons.addWidget(self.edit_supply_btn)
        supply_buttons.addWidget(self.delete_supply_btn)
        supply_buttons.addStretch()
        supply_buttons.addWidget(self.pdf_supply_btn)

        self.item_table = QTableWidget()
        self.item_table.setColumnCount(3)
        self.item_table.setHorizontalHeaderLabels(["Товар", "Количество", "ID"])
        self.item_table.setColumnHidden(2, True)

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
        top_layout.addWidget(self.supply_table)
        top_layout.addLayout(supply_buttons)
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

        self.add_supply_btn.clicked.connect(self.add_supply)
        self.edit_supply_btn.clicked.connect(self.edit_supply)
        self.delete_supply_btn.clicked.connect(self.delete_supply)
        self.pdf_supply_btn.clicked.connect(self.export_pdf)
        self.add_item_btn.clicked.connect(self.add_item)
        self.edit_item_btn.clicked.connect(self.edit_item)
        self.delete_item_btn.clicked.connect(self.delete_item)

        self.load_data()

    def get_selected_supply_id(self):
        row = self.supply_table.currentRow()
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
        self.current_ids = [r["supply_id"] for r in rows]
        self.supply_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.supply_table.setItem(i, 0, QTableWidgetItem(row.get("supplier_name", "—")))
            self.supply_table.setItem(i, 1, QTableWidgetItem(row.get("warehouse_address", "—")))
            d = row.get("supply_date")
            self.supply_table.setItem(i, 2, QTableWidgetItem(str(d) if d else "—"))
            self.supply_table.setItem(i, 3, QTableWidgetItem(str(row["supply_id"])))
        self.supply_table.resizeColumnsToContents()
        self.load_items()

    def load_items(self):
        supply_id = self.get_selected_supply_id()
        if not supply_id:
            self.item_table.setRowCount(0)
            self.current_item_ids = []
            return
        rows = self.repo.get_items(supply_id)
        self.current_item_ids = [r["income_id"] for r in rows]
        self.item_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.item_table.setItem(i, 0, QTableWidgetItem(row.get("item_name", "—")))
            self.item_table.setItem(i, 1, QTableWidgetItem(str(row.get("quantity", 0))))
            self.item_table.setItem(i, 2, QTableWidgetItem(str(row["income_id"])))
        self.item_table.resizeColumnsToContents()

    def on_supply_selected(self):
        self.load_items()

    def add_supply(self):
        suppliers = self.repo.get_all_suppliers()
        warehouses = self.repo.get_all_warehouses()
        dialog = SupplyDialog(self, suppliers=suppliers, warehouses=warehouses)
        if dialog.exec_():
            self.repo.create(dialog.get_data())
            self.load_data()

    def edit_supply(self):
        supply_id = self.get_selected_supply_id()
        if not supply_id:
            QMessageBox.warning(self, "Ошибка", "Выберите поставку")
            return
        data = self.repo.get_by_id(supply_id)
        suppliers = self.repo.get_all_suppliers()
        warehouses = self.repo.get_all_warehouses()
        dialog = SupplyDialog(self, data=data, suppliers=suppliers, warehouses=warehouses)
        if dialog.exec_():
            self.repo.update(supply_id, dialog.get_data())
            self.load_data()

    def delete_supply(self):
        supply_id = self.get_selected_supply_id()
        if not supply_id:
            QMessageBox.warning(self, "Ошибка", "Выберите поставку")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить поставку?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.repo.delete(supply_id)
            self.load_data()

    def add_item(self):
        supply_id = self.get_selected_supply_id()
        if not supply_id:
            QMessageBox.warning(self, "Ошибка", "Выберите поставку")
            return
        items = self.repo.get_all_items()
        dialog = SupplyItemDialog(self, items=items)
        if dialog.exec_():
            data = dialog.get_data()
            if data["item_id"] is None:
                QMessageBox.warning(self, "Ошибка", "Выберите товар")
                return
            self.repo.add_item(supply_id, data["item_id"], data["quantity"])
            self.load_items()

    def edit_item(self):
        income_id = self.get_selected_item_id()
        if not income_id:
            QMessageBox.warning(self, "Ошибка", "Выберите позицию")
            return
        supply_id = self.get_selected_supply_id()
        items = self.repo.get_all_items()
        data = {"item_id": None, "quantity": 0}
        for r in self.repo.get_items(supply_id):
            if r["income_id"] == income_id:
                data = r
                break
        dialog = SupplyItemDialog(self, items=items, data=data)
        if dialog.exec_():
            d = dialog.get_data()
            self.repo.update_item(income_id, d["quantity"])
            self.load_items()

    def delete_item(self):
        income_id = self.get_selected_item_id()
        if not income_id:
            QMessageBox.warning(self, "Ошибка", "Выберите позицию")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить позицию?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.repo.delete_item(income_id)
            self.load_items()

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "PDF — Поставки", "Поставки.pdf", "PDF Files (*.pdf)")
        if not path:
            return
        try:
            ReportService().supplies_report(path)
            import os; os.startfile(path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить PDF:\n{e}")
