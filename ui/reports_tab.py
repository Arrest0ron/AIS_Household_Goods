from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QTextEdit, QGroupBox,
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

        preview_actions = [
            ("Товары", self.preview_items),
            ("Категории", self.preview_categories),
            ("Поставщики", self.preview_suppliers),
            ("Поставки", self.preview_supplies),
            ("Покупатели", self.preview_customers),
            ("Заказы", self.preview_orders),
            ("Запасы", self.preview_stock),
            ("Малые остатки", self.preview_low_stock),
        ]

        preview_group = QGroupBox("Просмотр")
        preview_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        grid = QGridLayout()
        cols = 4
        for i, (label, method) in enumerate(preview_actions):
            b = QPushButton(label)
            b.setStyleSheet(style)
            b.clicked.connect(method)
            grid.addWidget(b, i // cols, i % cols)
        preview_group.setLayout(grid)

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

    def _items_html(self):
        rows = self.repo.get_all_items()
        html = "<h2>Товары</h2><table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;'>"
        html += "<tr><th>№</th><th>Название</th><th>Категория</th><th>Цена (₽)</th><th>Остаток</th><th>Масса (кг)</th></tr>"
        for i, r in enumerate(rows, 1):
            html += f"<tr><td>{i}</td><td>{r['item_name']}</td><td>{r.get('category_name') or '—'}</td>"
            html += f"<td>{float(r['price']):.2f}</td><td>{r['stock_quantity']}</td>"
            html += f"<td>{float(r['mass']):.2f}</td></tr>" if r.get('mass') else "<td>—</td></tr>"
        html += "</table>"
        return html

    def _categories_html(self):
        rows = self.repo.get_category_summary()
        html = "<h2>Категории</h2><table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;'>"
        html += "<tr><th>№</th><th>Категория</th><th>Товаров</th><th>Остаток</th><th>Стоимость (₽)</th></tr>"
        for i, r in enumerate(rows, 1):
            html += f"<tr><td>{i}</td><td>{r['category_name']}</td><td>{r['item_count']}</td>"
            html += f"<td>{r['total_stock']}</td><td>{float(r['total_value']):.2f}</td></tr>"
        html += "</table>"
        return html

    def _suppliers_html(self):
        rows = self.repo.get_all_suppliers()
        html = "<h2>Поставщики</h2><table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;'>"
        html += "<tr><th>№</th><th>Название</th><th>Контакты</th></tr>"
        for i, r in enumerate(rows, 1):
            html += f"<tr><td>{i}</td><td>{r['supplier_name']}</td><td>{r.get('contact_info') or '—'}</td></tr>"
        html += "</table>"
        return html

    def _supplies_html(self):
        rows = self.repo.get_supply_summary()
        html = "<h2>Поставки</h2><table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;'>"
        html += "<tr><th>№</th><th>Поставщик</th><th>Склад</th><th>Дата</th><th>Позиций</th><th>Кол-во</th></tr>"
        for i, r in enumerate(rows, 1):
            html += f"<tr><td>{i}</td><td>{r.get('supplier_name') or '—'}</td><td>{r.get('warehouse_address') or '—'}</td>"
            html += f"<td>{r['supply_date']}</td><td>{r['item_count']}</td><td>{r['total_items']}</td></tr>"
        html += "</table>"
        return html

    def _customers_html(self):
        rows = self.repo.get_all_customers()
        html = "<h2>Покупатели</h2><table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;'>"
        html += "<tr><th>№</th><th>Имя</th><th>Телефон</th><th>Email</th><th>Дата регистрации</th></tr>"
        for i, r in enumerate(rows, 1):
            html += f"<tr><td>{i}</td><td>{r['customer_name']}</td><td>{r.get('phone') or '—'}</td>"
            html += f"<td>{r.get('email') or '—'}</td><td>{r.get('registration_date') or '—'}</td></tr>"
        html += "</table>"
        return html

    def _orders_html(self):
        rows = self.repo.get_order_summary()
        html = "<h2>Заказы</h2><table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;'>"
        html += "<tr><th>№</th><th>Покупатель</th><th>Дата</th><th>Скидка</th><th>Сумма (₽)</th></tr>"
        for r in rows:
            html += f"<tr><td>{r['order_id']}</td><td>{r.get('customer_name') or '—'}</td>"
            html += f"<td>{r['order_date']}</td><td>{float(r['discount']):.2f}%</td>"
            html += f"<td>{float(r['total']):.2f}</td></tr>"
        html += "</table>"
        return html

    def _low_stock_html(self):
        rows = self.repo.get_low_stock_items(10)
        if not rows:
            return "<h2>Малые остатки</h2><p>Нет товаров с остатком <= 10</p>"
        html = "<h2>Малые остатки (<= 10)</h2><table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;'>"
        html += "<tr><th>№</th><th>Товар</th><th>Категория</th><th>Остаток</th><th>Цена (₽)</th></tr>"
        for i, r in enumerate(rows, 1):
            html += f"<tr><td>{i}</td><td>{r['item_name']}</td><td>{r.get('category_name') or '—'}</td>"
            html += f"<td>{r['stock_quantity']}</td><td>{float(r['price']):.2f}</td></tr>"
        html += "</table>"
        return html

    def preview_items(self): self.set_html(self._items_html())
    def preview_categories(self): self.set_html(self._categories_html())
    def preview_suppliers(self): self.set_html(self._suppliers_html())
    def preview_supplies(self): self.set_html(self._supplies_html())
    def preview_customers(self): self.set_html(self._customers_html())
    def preview_orders(self): self.set_html(self._orders_html())
    def preview_stock(self): self.set_html(self._items_html())
    def preview_low_stock(self): self.set_html(self._low_stock_html())

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
