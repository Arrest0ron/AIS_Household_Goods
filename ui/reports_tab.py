from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QGroupBox,
    QLabel, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QTextDocument, QPageSize
from PyQt6.QtPrintSupport import QPrinter
from repositories.report_repository import ReportRepository


class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.repo = ReportRepository()

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        style = "QPushButton { min-width: 140px; min-height: 28px; }"

        def make_group(title, buttons):
            g = QGroupBox(title)
            g.setStyleSheet("QGroupBox { font-weight: bold; }")
            layout = QHBoxLayout()
            for b in buttons:
                b.setStyleSheet(style)
                layout.addWidget(b)
            layout.addStretch()
            g.setLayout(layout)
            return g

        btn_summary = QPushButton("Обновить сводку")
        btn_summary.clicked.connect(self.show_summary)

        btn_pdf = QPushButton("Экспорт PDF")
        btn_pdf.clicked.connect(self.export_pdf)

        btn_stock = QPushButton("Запасы")
        btn_stock.setStyleSheet(style)
        btn_stock.clicked.connect(self.preview_stock)

        btn_low_stock = QPushButton("Малые остатки")
        btn_low_stock.setStyleSheet(style)
        btn_low_stock.clicked.connect(self.preview_low_stock)

        preview_group = QGroupBox("Отчёты")
        preview_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        preview_layout = QHBoxLayout()
        preview_layout.addWidget(btn_stock)
        preview_layout.addWidget(btn_low_stock)
        preview_layout.addStretch()
        preview_group.setLayout(preview_layout)

        layout = QVBoxLayout()
        layout.addWidget(make_group("Сводка", [btn_summary, btn_pdf]))
        layout.addWidget(preview_group)
        layout.addWidget(QLabel("Предпросмотр:"))
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        self.show_summary()

    def set_html(self, html):
        self.text_edit.setHtml(html)

    def show_summary(self):
        d = self.repo.get_summary()
        html = f"""
        <h2>Сводка по магазину</h2>
        <table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;">
        <tr><td><b>Категории</b></td><td>{d["categories_count"]}</td></tr>
        <tr><td><b>Товары</b></td><td>{d["items_count"]}</td></tr>
        <tr><td><b>Покупатели</b></td><td>{d["customers_count"]}</td></tr>
        <tr><td><b>Заказы</b></td><td>{d["orders_count"]}</td></tr>
        <tr><td><b>Поставки</b></td><td>{d["supplies_count"]}</td></tr>
        <tr><td><b>Общий остаток (шт.)</b></td><td>{d["total_stock"]}</td></tr>
        <tr><td><b>Стоимость запасов</b></td><td>{d["total_stock_value"]:.2f} ₽</td></tr>
        </table>
        """
        self.set_html(html)

    def preview_stock(self):
        rows = sorted(self.repo.get_all_items(), key=lambda r: r["stock_quantity"])
        html = "<h2>Складские запасы</h2><table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;'>"
        html += "<tr><th>№</th><th>Название</th><th>Категория</th><th>Цена (₽)</th><th>Остаток</th><th>Стоимость (₽)</th></tr>"
        for i, r in enumerate(rows, 1):
            price = float(r['price'])
            qty = r['stock_quantity']
            html += f"<tr><td>{i}</td><td>{r['item_name']}</td><td>{r.get('category_name') or '—'}</td>"
            html += f"<td>{price:.2f}</td><td>{qty}</td><td>{price * qty:.2f}</td></tr>"
        html += "</table>"
        self.set_html(html)

    def preview_low_stock(self):
        rows = self.repo.get_low_stock_items(10)
        if not rows:
            self.set_html("<h2>Малые остатки</h2><p>Нет товаров с остатком <= 10</p>")
            return
        html = "<h2>Малые остатки (<= 10)</h2><table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;'>"
        html += "<tr><th>№</th><th>Товар</th><th>Категория</th><th>Остаток</th><th>Цена (₽)</th></tr>"
        for i, r in enumerate(rows, 1):
            html += f"<tr><td>{i}</td><td>{r['item_name']}</td><td>{r.get('category_name') or '—'}</td>"
            html += f"<td>{r['stock_quantity']}</td><td>{float(r['price']):.2f}</td></tr>"
        html += "</table>"
        self.set_html(html)

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Экспорт PDF", "Отчёт.pdf", "PDF Files (*.pdf)")
        if not path:
            return
        try:
            doc = QTextDocument()
            doc.setHtml(self.text_edit.toHtml())
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(path)
            printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            doc.print(printer)
            import os; os.startfile(path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить PDF:\n{e}")
