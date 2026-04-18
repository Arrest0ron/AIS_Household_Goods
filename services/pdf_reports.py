import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate
from repositories.report_repository import ReportRepository
from datetime import datetime


class PDFReport:
    def __init__(self, title, landscape_mode=False):
        self.title = title
        self.landscape = landscape_mode
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            "Title_ru", parent=self.styles["Title"],
            fontSize=16, spaceAfter=6
        ))
        self.styles.add(ParagraphStyle(
            "Subtitle", parent=self.styles["Normal"],
            fontSize=9, textColor=colors.grey, alignment=TA_CENTER, spaceAfter=12
        ))
        self.styles.add(ParagraphStyle(
            "Cell", parent=self.styles["Normal"], fontSize=8, leading=10
        ))
        self.styles.add(ParagraphStyle(
            "HeaderCell", parent=self.styles["Normal"], fontSize=8,
            leading=10, alignment=TA_CENTER
        ))
        self.styles.add(ParagraphStyle(
            "Footer", parent=self.styles["Normal"], fontSize=7,
            textColor=colors.grey, alignment=TA_RIGHT
        ))
        self.elements = []

    def _header_footer(self, canvas, doc):
        canvas.saveState()
        w, h = doc.pagesize
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.grey)
        canvas.drawString(20*mm, 12*mm, f"АИС Магазин бытовых товаров — {self.title}")
        canvas.drawRightString(w - 20*mm, 12*mm, datetime.now().strftime("%d.%m.%Y %H:%M"))
        canvas.restoreState()

    def build(self, filepath):
        page_size = landscape(A4) if self.landscape else A4
        doc = SimpleDocTemplate(
            filepath, pagesize=page_size,
            topMargin=20*mm, bottomMargin=20*mm,
            leftMargin=15*mm, rightMargin=15*mm
        )
        template = PageTemplate(
            onPage=self._header_footer,
            frames=[Frame(
                15*mm, 20*mm,
                page_size[0] - 30*mm, page_size[1] - 40*mm,
                id="normal"
            )]
        )
        doc.addPageTemplates([template])
        doc.build(self.elements)

    def add_title(self, text):
        self.elements.append(Paragraph(text, self.styles["Title_ru"]))
        self.elements.append(Paragraph(
            f"Сформирован: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            self.styles["Subtitle"]
        ))
        self.elements.append(Spacer(1, 4*mm))

    def add_table(self, headers, rows, col_widths=None):
        data = [[Paragraph(h, self.styles["HeaderCell"]) for h in headers]]
        for row in rows:
            data.append([Paragraph(str(c), self.styles["Cell"]) for c in row])

        t = Table(data, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F5496")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D9D9D9")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F2F2")]),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        self.elements.append(t)
        self.elements.append(Spacer(1, 4*mm))

    def add_text(self, text):
        self.elements.append(Paragraph(text, self.styles["Normal"]))
        self.elements.append(Spacer(1, 2*mm))


class ReportService:
    def __init__(self):
        self.repo = ReportRepository()

    def categories_report(self, filepath):
        pdf = PDFReport("Категории товаров")
        pdf.add_title("Отчёт по категориям товаров")
        rows = self.repo.get_category_summary()
        headers = ["№", "Категория", "Товаров", "Остаток (шт.)", "Стоимость запасов (₽)"]
        data = [[
            i + 1, r["category_name"], r["item_count"],
            r["total_stock"], f'{float(r["total_value"]):.2f}'
        ] for i, r in enumerate(rows)]
        pdf.add_table(headers, data, col_widths=[20, 80, 50, 60, 80])
        pdf.build(filepath)

    def items_report(self, filepath):
        pdf = PDFReport("Товары", landscape_mode=True)
        pdf.add_title("Отчёт по товарам")
        rows = self.repo.get_all_items()
        headers = ["№", "Название", "Категория", "Цена (₽)", "Остаток", "Масса (кг)"]
        data = [[
            i + 1, r["item_name"], r.get("category_name") or "—",
            f'{float(r["price"]):.2f}', r["stock_quantity"],
            f'{float(r["mass"]):.2f}' if r.get("mass") else "—"
        ] for i, r in enumerate(rows)]
        pdf.add_table(headers, data, col_widths=[20, 120, 80, 60, 50, 50])
        pdf.build(filepath)

    def suppliers_report(self, filepath):
        pdf = PDFReport("Поставщики")
        pdf.add_title("Отчёт по поставщикам")
        rows = self.repo.get_all_suppliers()
        headers = ["№", "Название", "Контакты"]
        data = [[i + 1, r["supplier_name"], r.get("contact_info") or "—"]
                for i, r in enumerate(rows)]
        pdf.add_table(headers, data, col_widths=[20, 120, 200])
        pdf.build(filepath)

    def supplies_report(self, filepath):
        pdf = PDFReport("Поставки", landscape_mode=True)
        pdf.add_title("Отчёт по поставкам")
        rows = self.repo.get_supply_summary()
        headers = ["№", "Поставщик", "Склад", "Дата", "Позиций", "Кол-во товаров"]
        data = [[
            i + 1, r.get("supplier_name") or "—", r.get("warehouse_address") or "—",
            str(r["supply_date"]), r["item_count"], r["total_items"]
        ] for i, r in enumerate(rows)]
        pdf.add_table(headers, data, col_widths=[20, 100, 100, 60, 50, 60])
        pdf.build(filepath)

    def customers_report(self, filepath):
        pdf = PDFReport("Покупатели")
        pdf.add_title("Отчёт по покупателям")
        rows = self.repo.get_all_customers()
        headers = ["№", "Имя", "Телефон", "Email", "Дата регистрации"]
        data = [[
            i + 1, r["customer_name"], r.get("phone") or "—",
            r.get("email") or "—", str(r.get("registration_date") or "—")
        ] for i, r in enumerate(rows)]
        pdf.add_table(headers, data, col_widths=[20, 100, 100, 120, 80])
        pdf.build(filepath)

    def orders_report(self, filepath):
        pdf = PDFReport("Заказы", landscape_mode=True)
        pdf.add_title("Отчёт по заказам")
        rows = self.repo.get_order_summary()
        headers = ["№", "Покупатель", "Дата", "Скидка", "Сумма (₽)"]
        data = [[
            r["order_id"], r.get("customer_name") or "—",
            str(r["order_date"]), f'{float(r["discount"]):.2f}%',
            f'{float(r["total"]):.2f}'
        ] for r in rows]
        pdf.add_table(headers, data, col_widths=[30, 120, 70, 50, 80])
        pdf.build(filepath)

    def stock_report(self, filepath):
        pdf = PDFReport("Складские запасы", landscape_mode=True)
        pdf.add_title("Отчёт по складским запасам")
        rows = sorted(self.repo.get_all_items(), key=lambda r: r["stock_quantity"])
        headers = ["№", "Название", "Категория", "Цена (₽)", "Остаток", "Стоимость (₽)"]
        data = [[
            i + 1, r["item_name"], r.get("category_name") or "—",
            f'{float(r["price"]):.2f}', r["stock_quantity"],
            f'{float(r["price"]) * r["stock_quantity"]:.2f}'
        ] for i, r in enumerate(rows)]
        pdf.add_table(headers, data, col_widths=[20, 120, 80, 60, 50, 70])
        pdf.build(filepath)

    def low_stock_report(self, filepath, threshold=10):
        pdf = PDFReport("Малые остатки")
        pdf.add_title(f"Отчёт по товарам с остатком ≤ {threshold}")
        rows = self.repo.get_low_stock_items(threshold)
        if not rows:
            pdf.add_text(f"Нет товаров с остатком ≤ {threshold}")
            pdf.build(filepath)
            return
        headers = ["№", "Товар", "Категория", "Остаток", "Цена (₽)"]
        data = [[
            i + 1, r["item_name"], r.get("category_name") or "—",
            r["stock_quantity"], f'{float(r["price"]):.2f}'
        ] for i, r in enumerate(rows)]
        pdf.add_table(headers, data, col_widths=[20, 120, 80, 50, 60])
        pdf.build(filepath)
