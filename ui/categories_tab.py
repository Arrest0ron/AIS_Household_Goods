from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog, QComboBox
)
from repositories.category_repository import CategoryRepository
from ui.dialogs import CategoryDialog
from services.pdf_reports import ReportService
import logging

log = logging.getLogger("ui.categories")


class CategoriesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.repo = CategoryRepository()
        self.current_ids = []

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию")

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Все", "Только 18+", "Без 18+"])
        self.filter_combo.currentIndexChanged.connect(self.apply_filter)

        self.search_btn = QPushButton("Найти")
        self.add_btn = QPushButton("Добавить")
        self.edit_btn = QPushButton("Изменить")
        self.delete_btn = QPushButton("Удалить")
        self.pdf_btn = QPushButton("PDF")

        headers = ["Название", "18+"]
        self.table = QTableWidget()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
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
        self.current_ids = [row["category_id"] for row in rows]
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(row.get("category_name", "")))
            self.table.setItem(i, 1, QTableWidgetItem("Да" if row.get("adult_flag") else "Нет"))
        self.table.resizeColumnsToContents()

    def add(self):
        log.info("Открываем диалог добавления категории")
        try:
            dialog = CategoryDialog(self)
            log.info("CategoryDialog создан")
        except Exception:
            log.exception("Ошибка при создании CategoryDialog")
            return
        try:
            result = dialog.exec()
            log.info("dialog.exec() вернул: %s", result)
        except Exception:
            log.exception("Ошибка при dialog.exec()")
            return
        if result:
            data = dialog.get_data()
            if not data["category_name"]:
                QMessageBox.warning(self, "Ошибка", "Введите название категории")
                return
            self.repo.create(data)
            QMessageBox.information(self, "Успех", "Категория добавлена")
            self.load_data()

    def edit(self):
        category_id = self.get_selected_id()
        if not category_id:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию")
            return
        try:
            data = self.repo.get_by_id(category_id)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные:\n{e}")
            return
        dialog = CategoryDialog(self, data=data)
        if dialog.exec():
            data = dialog.get_data()
            if not data["category_name"]:
                QMessageBox.warning(self, "Ошибка", "Введите название категории")
                return
            try:
                self.repo.update(category_id, data)
                QMessageBox.information(self, "Успех", "Категория обновлена")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить:\n{e}")

    def delete(self):
        category_id = self.get_selected_id()
        if not category_id:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить категорию?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.repo.delete(category_id)
            self.load_data()

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "PDF — Категории", "Категории.pdf", "PDF Files (*.pdf)")
        if not path:
            return
        try:
            ReportService().categories_report(path)
            import os; os.startfile(path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить PDF:\n{e}")
