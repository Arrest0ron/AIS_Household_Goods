from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog, QComboBox
)
from repositories.item_repository import ItemRepository
from ui.dialogs import ItemDialog
from services.pdf_reports import ReportService


class ItemsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.repo = ItemRepository()
        self.current_ids = []

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию")

        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Все категории")
        self.filter_combo.currentIndexChanged.connect(self.apply_filter)

        self.search_btn = QPushButton("Найти")
        self.add_btn = QPushButton("Добавить")
        self.edit_btn = QPushButton("Изменить")
        self.delete_btn = QPushButton("Удалить")
        self.pdf_btn = QPushButton("PDF")

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Название", "Категория", "Цена", "Остаток", "Масса (кг)"])
        self.table.setSortingEnabled(True)

        top = QHBoxLayout()
        top.addWidget(self.search_input)
        top.addWidget(self.search_btn)
        top.addWidget(self.filter_combo)
        top.addWidget(self.add_btn)
        top.addWidget(self.edit_btn)
        top.addWidget(self.delete_btn)
        top.addStretch()
        top.addWidget(self.pdf_btn)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.search_btn.clicked.connect(self.search)
        self.add_btn.clicked.connect(self.add)
        self.edit_btn.clicked.connect(self.edit)
        self.delete_btn.clicked.connect(self.delete)
        self.pdf_btn.clicked.connect(self.export_pdf)

        self.load_data()

    def get_selected_id(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.current_ids):
            return None
        return self.current_ids[row]

    def load_data(self):
        cats = self.repo.get_categories()
        self.filter_combo.blockSignals(True)
        current = self.filter_combo.currentText()
        self.filter_combo.clear()
        self.filter_combo.addItem("Все категории")
        for c in cats:
            self.filter_combo.addItem(c["category_name"], c["category_id"])
        idx = self.filter_combo.findText(current)
        if idx >= 0:
            self.filter_combo.setCurrentIndex(idx)
        self.filter_combo.blockSignals(False)
        self.fill_table(self.repo.get_all())

    def search(self):
        text = self.search_input.text().strip()
        rows = self.repo.search(text) if text else self.repo.get_all()
        self.fill_table(self._apply_category_filter(rows))

    def apply_filter(self):
        self.search()

    def _apply_category_filter(self, rows):
        cat_id = self.filter_combo.currentData()
        if cat_id:
            return [r for r in rows if r.get("category_id") == cat_id]
        return rows

    def fill_table(self, rows):
        self.current_ids = [row["item_id"] for row in rows]
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(row.get("item_name", "")))
            self.table.setItem(i, 1, QTableWidgetItem(row.get("category_name") or "—"))
            self.table.setItem(i, 2, QTableWidgetItem(f'{row.get("price", 0):.2f}'))
            self.table.setItem(i, 3, QTableWidgetItem(str(row.get("stock_quantity", 0))))
            mass = row.get("mass")
            self.table.setItem(i, 4, QTableWidgetItem(f"{mass:.2f}" if mass else "—"))
        self.table.resizeColumnsToContents()

    def add(self):
        cats = self.repo.get_categories()
        dialog = ItemDialog(self, categories=cats)
        if dialog.exec():
            self.repo.create(dialog.get_data())
            self.load_data()

    def edit(self):
        item_id = self.get_selected_id()
        if not item_id:
            QMessageBox.warning(self, "Ошибка", "Выберите товар")
            return
        try:
            data = self.repo.get_by_id(item_id)
            cats = self.repo.get_categories()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные:\n{e}")
            return
        dialog = ItemDialog(self, data=data, categories=cats)
        if dialog.exec():
            try:
                self.repo.update(item_id, dialog.get_data())
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить:\n{e}")

    def delete(self):
        item_id = self.get_selected_id()
        if not item_id:
            QMessageBox.warning(self, "Ошибка", "Выберите товар")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить товар?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.repo.delete(item_id)
            self.load_data()

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "PDF — Товары", "Товары.pdf", "PDF Files (*.pdf)")
        if not path:
            return
        try:
            ReportService().items_report(path)
            import os; os.startfile(path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить PDF:\n{e}")
