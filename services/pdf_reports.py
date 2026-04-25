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
from repositories.supply_repository import SupplyRepository
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

    def supply_contract(self, filepath, supply_id):
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import Paragraph, Spacer, Table
        from reportlab.lib.units import mm

        supply_repo = SupplyRepository()
        supply = supply_repo.get_supply_detail(supply_id)
        if not supply:
            raise ValueError(f"Поставка #{supply_id} не найдена")

        items = supply_repo.get_items_with_prices(supply_id)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle("ContractTitle",
            fontSize=16, spaceAfter=4, alignment=TA_CENTER,
            fontName="Helvetica-Bold")
        subtitle_style = ParagraphStyle("ContractSub",
            fontSize=10, alignment=TA_CENTER, spaceAfter=20)
        normal = ParagraphStyle("ContractNormal",
            fontSize=10, leading=14, spaceAfter=4)
        bold_style = ParagraphStyle("ContractBold", parent=normal,
            fontName="Helvetica-Bold", spaceAfter=10)
        sig_style = ParagraphStyle("Signature",
            fontSize=10, leading=14, spaceBefore=30)
        hdr_style = ParagraphStyle("H", fontSize=9,
            fontName="Helvetica-Bold", alignment=TA_CENTER)
        cell_style = ParagraphStyle("Cell", fontSize=9)
        cell_center = ParagraphStyle("CellCenter", parent=cell_style,
            alignment=TA_CENTER)

        elements = []

        elements.append(Paragraph("ДОГОВОР ПОСТАВКИ", title_style))
        elements.append(Paragraph(f"№ {supply_id}  от  {supply['supply_date']}", subtitle_style))
        elements.append(Paragraph("г. Москва", subtitle_style))
        elements.append(Spacer(1, 6*mm))

        elements.append(Paragraph(
            f'<b>Поставщик:</b> {supply["supplier_name"]}', normal))
        if supply.get("contact_info"):
            elements.append(Paragraph(
                f'<b>Контактные данные:</b> {supply["contact_info"]}', normal))
        elements.append(Paragraph(
            f'<b>Склад отгрузки:</b> {supply["warehouse_address"]}', normal))
        elements.append(Spacer(1, 4*mm))

        elements.append(Paragraph(
            "Настоящий Договор составлен о том, что Поставщик обязуется "
            "передать, а Покупатель — принять и оплатить следующий товар:",
            normal))
        elements.append(Spacer(1, 4*mm))

        headers = ["№", "Наименование", "Кол-во", "Цена (₽)", "Сумма (₽)"]
        data = [[Paragraph(h, hdr_style) for h in headers]]

        total = 0
        for i, item in enumerate(items):
            qty = item["quantity"]
            price = float(item["price"]) if item.get("price") else 0
            amount = qty * price
            total += amount
            data.append([
                Paragraph(str(i + 1), cell_center),
                Paragraph(item["item_name"], cell_style),
                Paragraph(str(qty), cell_center),
                Paragraph(f"{price:.2f}", cell_center),
                Paragraph(f"{amount:.2f}", cell_center),
            ])

        total_bold_center = ParagraphStyle("TotalBoldCenter",
            fontSize=9, fontName="Helvetica-Bold", alignment=TA_CENTER)
        data.append([
            Paragraph("", cell_center),
            Paragraph("<b>ИТОГО:</b>", total_bold_center),
            Paragraph("", cell_center),
            Paragraph("", cell_center),
            Paragraph(f"<b>{total:.2f}</b>", total_bold_center),
        ])

        t = Table(data, colWidths=[20, 170, 50, 60, 60], repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F5496")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -2), 0.5, colors.HexColor("#D9D9D9")),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#E8E0F7")),
            ("GRID", (0, -1), (-1, -1), 0.5, colors.HexColor("#2F5496")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 10*mm))

        elements.append(Paragraph(
            f"<b>Общая сумма Договора:</b> {total:,.2f} руб.",
            bold_style))
        elements.append(Spacer(1, 10*mm))

        sig_table = Table([
            [Paragraph("Поставщик:", sig_style),
             Paragraph("Покупатель:", sig_style)],
            [Paragraph("_____________ /______________/", sig_style),
             Paragraph("_____________ /______________/", sig_style)],
            [Paragraph("М.П.", sig_style),
             Paragraph("М.П.", sig_style)],
        ], colWidths=[90*mm, 90*mm])
        sig_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
        elements.append(sig_table)

        doc = SimpleDocTemplate(filepath, pagesize=A4,
            topMargin=20*mm, bottomMargin=20*mm,
            leftMargin=20*mm, rightMargin=20*mm)
        template = PageTemplate(
            onPage=lambda c, d: None,
            frames=[Frame(20*mm, 20*mm, A4[0] - 40*mm,
                          A4[1] - 40*mm, id="normal")])
        doc.addPageTemplates([template])
        doc.build(elements)
