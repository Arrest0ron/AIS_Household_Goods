from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
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
        self.pdf_btn = QPushButton("PDF")

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Название", "Категория", "Цена (₽)", "Остаток", "Масса (кг)"])

        top = QHBoxLayout()
        top.addWidget(self.search_input)
        top.addWidget(self.search_btn)
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
        self.fill_table(self.repo.get_all())

    def search(self):
        text = self.search_input.text().strip()
        self.fill_table(self.repo.search(text) if text else self.repo.get_all())

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
