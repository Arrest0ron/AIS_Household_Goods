from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QComboBox
)
from repositories.category_repository import CategoryRepository
from services.pdf_reports import ReportService


class UserCategoriesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.repo = CategoryRepository()
        self.pdf_service = ReportService()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию")
        self.search_btn = QPushButton("Найти")

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Все", "Только 18+", "Без 18+"])
        self.filter_combo.currentIndexChanged.connect(self.apply_filter)

        self.pdf_btn = QPushButton("PDF")

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Название", "18+"])
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
        rows = self.repo.get_all()
        self.fill_table(rows)

    def search(self):
        text = self.search_input.text().strip()
        rows = self.repo.search(text) if text else self.repo.get_all()
        self.fill_table(self._apply_adult_filter(rows))

    def apply_filter(self):
        self.search()

    def _apply_adult_filter(self, rows):
        idx = self.filter_combo.currentIndex()
        if idx == 1:
            return [r for r in rows if r.get("adult_flag")]
        elif idx == 2:
            return [r for r in rows if not r.get("adult_flag")]
        return rows

    def fill_table(self, rows):
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(row.get("category_name", "")))
            self.table.setItem(i, 1, QTableWidgetItem("Да" if row.get("adult_flag") else "Нет"))
        self.table.resizeColumnsToContents()

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить PDF — Категории", "Категории.pdf", "PDF Files (*.pdf)")
        if not path:
            return
        try:
            self.pdf_service.categories_report(path)
            QMessageBox.information(self, "Успех", f"PDF сохранён:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить PDF:\n{e}")
