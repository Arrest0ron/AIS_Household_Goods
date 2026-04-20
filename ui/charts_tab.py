import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QGridLayout, QFrame, QSizePolicy, QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as mticker
from repositories.report_repository import ReportRepository

log = logging.getLogger("ui.charts")

PURPLE_PALETTE = [
    "#7C3AED", "#6D28D9", "#8B5CF6", "#A78BFA",
    "#C4B5FD", "#5B21B6", "#4C1D95", "#DDD6FE",
    "#EDE4FF", "#D8CCF0",
]

KPI_COLORS = [
    ("#7C3AED", "#F3EEFF"),
    ("#10B981", "#ECFDF5"),
    ("#F59E0B", "#FFFBEB"),
    ("#3B82F6", "#EFF6FF"),
    ("#D946EF", "#FDF4FF"),
]


class ChartsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.repo = ReportRepository()
        self._setup_ui()
        self.refresh_charts()

    def _setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(12)

        top_row = QHBoxLayout()
        self.refresh_btn = QPushButton("Обновить графики")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background: #7C3AED; color: #fff; border: none;
                padding: 10px 24px; border-radius: 8px;
                font-weight: 700; font-size: 11pt;
            }
            QPushButton:hover { background: #6D28D9; }
        """)
        self.refresh_btn.clicked.connect(self.refresh_charts)

        top_row.addStretch()
        top_row.addWidget(self.refresh_btn)
        main_layout.addLayout(top_row)

        self.kpi_layout = QHBoxLayout()
        self.kpi_layout.setSpacing(12)
        main_layout.addLayout(self.kpi_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        charts_container = QWidget()
        self.charts_layout = QGridLayout(charts_container)
        self.charts_layout.setSpacing(16)
        self.chart_widgets = []
        scroll.setWidget(charts_container)
        main_layout.addWidget(scroll, 1)

        self.low_stock_group = QFrame()
        self.low_stock_group.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border: 1px solid #D8CCF0;
                border-radius: 10px;
            }
        """)
        low_layout = QVBoxLayout(self.low_stock_group)
        low_layout.setContentsMargins(12, 8, 12, 8)
        low_title = QLabel("Малые остатки (<= 10 шт)")
        low_title.setStyleSheet("color: #6D28D9; font-weight: 700; font-size: 10pt; border: none;")
        low_layout.addWidget(low_title)
        self.low_stock_canvas = None
        main_layout.addWidget(self.low_stock_group)

        self.setLayout(main_layout)

    def _make_kpi_card(self, label_text, value_text, colors):
        border_color, bg_color = colors
        frame = QFrame()
        frame.setFixedHeight(90)
        frame.setMinimumWidth(160)
        frame.setStyleSheet(f"""
            QFrame {{
                background: {bg_color};
                border-left: 4px solid {border_color};
                border-radius: 8px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(4)
        val = QLabel(str(value_text))
        val.setStyleSheet(f"color: {border_color}; font-size: 18pt; font-weight: 800; border: none; background: transparent;")
        val.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lbl = QLabel(label_text)
        lbl.setStyleSheet("color: #4A2D8A; font-size: 9pt; font-weight: 600; border: none; background: transparent;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(val)
        layout.addWidget(lbl)
        return frame

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def _create_chart_widget(self, title):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border: 1px solid #D8CCF0;
                border-radius: 10px;
            }
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(8, 8, 8, 8)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #6D28D9; font-weight: 700; font-size: 10pt; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_lbl)
        fig = Figure(figsize=(5, 3.5), dpi=100)
        fig.patch.set_facecolor("#FFFFFF")
        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(canvas, 1)
        return frame, fig, canvas

    def _style_chart(self, fig, ax):
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")
        ax.tick_params(colors="#2D1B69", labelsize=8)
        for spine in ax.spines.values():
            spine.set_color("#D8CCF0")
        ax.grid(True, alpha=0.3, color="#C4B5FD")

    def refresh_charts(self):
        try:
            self._clear_layout(self.kpi_layout)
            for w in self.chart_widgets:
                w.deleteLater()
            self.chart_widgets.clear()

            summary = self.repo.get_summary()
            kpi_data = [
                ("Категории", summary.get("categories_count", 0)),
                ("Товары", summary.get("items_count", 0)),
                ("Заказы", summary.get("orders_count", 0)),
                ("Клиенты", summary.get("customers_count", 0)),
                ("Стоимость", f"{summary.get('total_stock_value', 0):,.0f} ₽"),
            ]
            for i, (lbl, val) in enumerate(kpi_data):
                card = self._make_kpi_card(lbl, val, KPI_COLORS[i])
                self.kpi_layout.addWidget(card)
            self.kpi_layout.addStretch()

            cat_data = self.repo.get_category_summary()
            self._draw_category_pie(cat_data)
            self._draw_stock_bar(cat_data)

            order_data = self.repo.get_order_summary()
            self._draw_orders_bar(order_data)

            supply_data = self.repo.get_supply_summary()
            self._draw_supplies_bar(supply_data)

            self._draw_low_stock()

            log.info("Графики обновлены")

        except Exception:
            log.exception("Ошибка при обновлении графиков")
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные для графиков.")

    def _draw_category_pie(self, data):
        frame, fig, canvas = self._create_chart_widget("Товары по категориям")
        self.charts_layout.addWidget(frame, 0, 0)
        self.chart_widgets.append(frame)
        ax = fig.add_subplot(111)
        self._style_chart(fig, ax)
        labels = [d["category_name"] for d in data]
        sizes = [d["item_count"] for d in data]
        if not any(sizes):
            ax.text(0.5, 0.5, "Нет данных", ha="center", va="center",
                    fontsize=14, color="#9A84C7", transform=ax.transAxes)
            ax.axis("off")
            canvas.draw()
            return
        colors = PURPLE_PALETTE[:len(labels)]
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct="%1.0f%%",
            colors=colors, startangle=90,
            textprops={"fontsize": 8, "color": "#2D1B69"},
        )
        for t in autotexts:
            t.set_fontsize(7)
            t.set_color("#FFFFFF")
            t.set_fontweight("bold")
        ax.set_title("")
        canvas.draw()

    def _draw_stock_bar(self, data):
        frame, fig, canvas = self._create_chart_widget("Стоимость запасов по категориям (₽)")
        self.charts_layout.addWidget(frame, 0, 1)
        self.chart_widgets.append(frame)
        ax = fig.add_subplot(111)
        self._style_chart(fig, ax)
        labels = [d["category_name"] for d in data]
        values = [float(d["total_value"]) for d in data]
        if not any(values):
            ax.text(0.5, 0.5, "Нет данных", ha="center", va="center",
                    fontsize=14, color="#9A84C7", transform=ax.transAxes)
            ax.axis("off")
            canvas.draw()
            return
        bars = ax.bar(labels, values, color=PURPLE_PALETTE[:len(labels)], edgecolor="#FFFFFF", linewidth=0.5)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=8)
        for bar, val in zip(bars, values):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                        f"{val:,.0f}", ha="center", va="bottom", fontsize=7, color="#2D1B69")
        fig.tight_layout()
        canvas.draw()

    def _draw_orders_bar(self, data):
        frame, fig, canvas = self._create_chart_widget("Заказы (сумма ₽)")
        self.charts_layout.addWidget(frame, 1, 0)
        self.chart_widgets.append(frame)
        ax = fig.add_subplot(111)
        self._style_chart(fig, ax)
        dates = [str(d["order_date"]) if d["order_date"] else "—" for d in data]
        totals = [float(d["total"]) for d in data]
        if not any(totals):
            ax.text(0.5, 0.5, "Нет данных", ha="center", va="center",
                    fontsize=14, color="#9A84C7", transform=ax.transAxes)
            ax.axis("off")
            canvas.draw()
            return
        labels = [f"#{d['order_id']}" for d in data]
        bars = ax.bar(labels, totals, color="#7C3AED", edgecolor="#FFFFFF", linewidth=0.5)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=7)
        for bar, val in zip(bars, totals):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                        f"{val:,.0f}", ha="center", va="bottom", fontsize=7, color="#2D1B69")
        fig.tight_layout()
        canvas.draw()

    def _draw_supplies_bar(self, data):
        frame, fig, canvas = self._create_chart_widget("Поставки (кол-во товаров)")
        self.charts_layout.addWidget(frame, 1, 1)
        self.chart_widgets.append(frame)
        ax = fig.add_subplot(111)
        self._style_chart(fig, ax)
        labels = [f"#{d['supply_id']}" for d in data]
        quantities = [int(d["total_items"]) for d in data]
        if not any(quantities):
            ax.text(0.5, 0.5, "Нет данных", ha="center", va="center",
                    fontsize=14, color="#9A84C7", transform=ax.transAxes)
            ax.axis("off")
            canvas.draw()
            return
        bars = ax.bar(labels, quantities, color="#6D28D9", edgecolor="#FFFFFF", linewidth=0.5)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=7)
        for bar, val in zip(bars, quantities):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                        str(val), ha="center", va="bottom", fontsize=7, color="#2D1B69")
        fig.tight_layout()
        canvas.draw()

    def _draw_low_stock(self):
        while self.low_stock_group.layout().count() > 1:
            item = self.low_stock_group.layout().takeAt(1)
            w = item.widget()
            if w:
                w.deleteLater()
        try:
            items = self.repo.get_low_stock_items(10)
        except Exception:
            log.exception("Ошибка загрузки малых остатков")
            items = []

        if not items:
            lbl = QLabel("Все товары в достаточном количестве")
            lbl.setStyleSheet("color: #10B981; font-weight: 600; padding: 8px; border: none;")
            self.low_stock_group.layout().addWidget(lbl)
            return

        fig = Figure(figsize=(8, max(2, len(items) * 0.5)), dpi=100)
        fig.patch.set_facecolor("#FFFFFF")
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        self._style_chart(fig, ax)
        names = [d["item_name"] for d in items]
        quantities = [int(d["stock_quantity"]) for d in items]
        colors = ["#F43F5E" if q == 0 else "#F59E0B" for q in quantities]
        bars = ax.barh(names, quantities, color=colors, edgecolor="#FFFFFF", height=0.6)
        ax.set_xlabel("Кол-во", fontsize=8, color="#2D1B69")
        for bar, val in zip(bars, quantities):
            ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                    str(val), ha="left", va="center", fontsize=8, color="#2D1B69", fontweight="bold")
        ax.invert_yaxis()
        fig.tight_layout()
        self.low_stock_group.layout().addWidget(canvas)
