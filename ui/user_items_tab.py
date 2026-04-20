from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QComboBox
)
from repositories.item_repository import ItemRepository
from services.pdf_reports import ReportService


class UserItemsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.repo = ItemRepository()
        self.pdf_service = ReportService()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию")
        self.search_btn = QPushButton("Найти")

        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Все категории")
        self.filter_combo.currentIndexChanged.connect(self.apply_filter)

        self.pdf_btn = QPushButton("PDF")

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Название", "Категория", "Цена (₽)", "Остаток", "Масса (кг)"])
        self.table.setSortingEnabled(True)

        top = QHBoxLayout()
        top.addWidget(self.search_input)
        top.addWidget(self.search_btn)
        top.addWidget(self.filter_combo)
        top.addStretch()
        top.addWidget(self.pdf_btn)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.search_btn.clicked.connect(self.search)
        self.pdf_btn.clicked.connect(self.export_pdf)

        self.load_data()

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
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(row.get("item_name", "")))
            self.table.setItem(i, 1, QTableWidgetItem(row.get("category_name") or "—"))
            self.table.setItem(i, 2, QTableWidgetItem(f'{row.get("price", 0):.2f}'))
            self.table.setItem(i, 3, QTableWidgetItem(str(row.get("stock_quantity", 0))))
            mass = row.get("mass")
            self.table.setItem(i, 4, QTableWidgetItem(f"{mass:.2f}" if mass else "—"))
        self.table.resizeColumnsToContents()

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить PDF — Товары", "Товары.pdf", "PDF Files (*.pdf)")
        if not path:
            return
        try:
            self.pdf_service.items_report(path)
            QMessageBox.information(self, "Успех", f"PDF сохранён:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить PDF:\n{e}")
