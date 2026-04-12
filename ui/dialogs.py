from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QTextEdit
)
from PyQt6.QtCore import QDate, QTime


class BaseDialog(QDialog):
    def __init__(self, title, parent=None, data=None, width=400, height=150):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(width, height)
        self.form = QFormLayout()

        btn_ok = QPushButton("Сохранить")
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Отмена")
        btn_cancel.clicked.connect(self.reject)

        buttons = QHBoxLayout()
        buttons.addWidget(btn_ok)
        buttons.addWidget(btn_cancel)

        layout = QVBoxLayout()
        layout.addLayout(self.form)
        layout.addLayout(buttons)
        self.setLayout(layout)

    def add_row(self, label, widget):
        self.form.addRow(label + ":", widget)

    def get_yes_no(self, value):
        return "Да" if value else "Нет"

    def set_yes_no(self, combo, value):
        combo.setCurrentText("Да" if value else "Нет")


class CategoryDialog(BaseDialog):
    def __init__(self, parent=None, data=None):
        super().__init__("Категория", parent, data)
        self.name_edit = QLineEdit()
        self.adult_combo = QComboBox()
        self.adult_combo.addItems(["Нет", "Да"])
        self.add_row("Название", self.name_edit)
        self.add_row("18+", self.adult_combo)
        if data:
            self.name_edit.setText(data.get("category_name") or "")
            self.set_yes_no(self.adult_combo, data.get("adult_flag"))

    def get_data(self):
        return {
            "category_name": self.name_edit.text().strip(),
            "adult_flag": self.adult_combo.currentText() == "Да"
        }


class WarehouseDialog(BaseDialog):
    def __init__(self, parent=None, data=None):
        super().__init__("Склад", parent, data, height=180)
        self.address_edit = QLineEdit()
        self.capacity_spin = QSpinBox()
        self.capacity_spin.setRange(0, 999999)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Основной", "Дополнительный", "Малый"])
        self.add_row("Адрес", self.address_edit)
        self.add_row("Вместимость", self.capacity_spin)
        self.add_row("Тип", self.type_combo)
        if data:
            self.address_edit.setText(data.get("warehouse_address") or "")
            self.capacity_spin.setValue(data.get("capacity") or 0)
            self.type_combo.setCurrentText(data.get("type") or "Основной")

    def get_data(self):
        return {
            "warehouse_address": self.address_edit.text().strip(),
            "capacity": self.capacity_spin.value(),
            "type": self.type_combo.currentText()
        }


class SupplierDialog(BaseDialog):
    def __init__(self, parent=None, data=None):
        super().__init__("Поставщик", parent, data, height=160)
        self.name_edit = QLineEdit()
        self.contact_edit = QLineEdit()
        self.add_row("Название", self.name_edit)
        self.add_row("Контакты", self.contact_edit)
        if data:
            self.name_edit.setText(data.get("supplier_name") or "")
            self.contact_edit.setText(data.get("contact_info") or "")

    def get_data(self):
        return {
            "supplier_name": self.name_edit.text().strip(),
            "contact_info": self.contact_edit.text().strip()
        }


class CustomerDialog(BaseDialog):
    def __init__(self, parent=None, data=None):
        super().__init__("Покупатель", parent, data, height=170)
        self.name_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.add_row("Имя", self.name_edit)
        self.add_row("Телефон", self.phone_edit)
        self.add_row("Email", self.email_edit)
        if data:
            self.name_edit.setText(data.get("customer_name") or "")
            self.phone_edit.setText(data.get("phone") or "")
            self.email_edit.setText(data.get("email") or "")

    def get_data(self):
        return {
            "customer_name": self.name_edit.text().strip(),
            "phone": self.phone_edit.text().strip(),
            "email": self.email_edit.text().strip()
        }


class ItemDialog(BaseDialog):
    def __init__(self, parent=None, data=None, categories=None):
        super().__init__("Товар", parent, data, height=220)
        self.name_edit = QLineEdit()
        self.category_combo = QComboBox()
        self.category_combo.addItem("— Без категории —", None)
        self._categories = categories or []
        for cat in self._categories:
            self.category_combo.addItem(cat["category_name"], cat["category_id"])
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0, 999999)
        self.price_spin.setDecimals(2)
        self.stock_spin = QSpinBox()
        self.stock_spin.setRange(0, 999999)
        self.mass_spin = QDoubleSpinBox()
        self.mass_spin.setRange(0, 999999)
        self.mass_spin.setDecimals(2)
        self.mass_spin.setSpecialValueText("—")
        self.add_row("Название", self.name_edit)
        self.add_row("Категория", self.category_combo)
        self.add_row("Цена", self.price_spin)
        self.add_row("Остаток", self.stock_spin)
        self.add_row("Масса (кг)", self.mass_spin)
        if data:
            self.name_edit.setText(data.get("item_name") or "")
            self.price_spin.setValue(float(data.get("price") or 0))
            self.stock_spin.setValue(data.get("stock_quantity") or 0)
            self.mass_spin.setValue(float(data.get("mass") or 0) if data.get("mass") else 0)
            cat_id = data.get("category_id")
            idx = self.category_combo.findData(cat_id)
            if idx >= 0:
                self.category_combo.setCurrentIndex(idx)

    def get_data(self):
        return {
            "item_name": self.name_edit.text().strip(),
            "category_id": self.category_combo.currentData(),
            "price": self.price_spin.value(),
            "stock_quantity": self.stock_spin.value(),
            "mass": self.mass_spin.value() if self.mass_spin.value() > 0 else None
        }


class SupplyDialog(BaseDialog):
    def __init__(self, parent=None, data=None, suppliers=None, warehouses=None):
        super().__init__("Поставка", parent, data, height=170)
        self.supplier_combo = QComboBox()
        self._suppliers = suppliers or []
        for s in self._suppliers:
            self.supplier_combo.addItem(s["supplier_name"], s["supplier_id"])
        self.warehouse_combo = QComboBox()
        self._warehouses = warehouses or []
        for w in self._warehouses:
            self.warehouse_combo.addItem(f'{w["warehouse_address"]} ({w["type"]})', w["warehouse_id"])
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.add_row("Поставщик", self.supplier_combo)
        self.add_row("Склад", self.warehouse_combo)
        self.add_row("Дата", self.date_edit)
        if data:
            idx = self.supplier_combo.findData(data.get("supplier_id"))
            if idx >= 0:
                self.supplier_combo.setCurrentIndex(idx)
            idx = self.warehouse_combo.findData(data.get("warehouse_id"))
            if idx >= 0:
                self.warehouse_combo.setCurrentIndex(idx)
            if data.get("supply_date"):
                self.date_edit.setDate(QDate.fromString(str(data["supply_date"]), "yyyy-MM-dd"))

    def get_data(self):
        return {
            "supplier_id": self.supplier_combo.currentData(),
            "warehouse_id": self.warehouse_combo.currentData(),
            "supply_date": self.date_edit.date().toString("yyyy-MM-dd")
        }


class OrderDialog(BaseDialog):
    def __init__(self, parent=None, data=None, customers=None):
        super().__init__("Заказ", parent, data, height=220)
        self.customer_combo = QComboBox()
        self._customers = customers or []
        for c in self._customers:
            self.customer_combo.addItem(c["customer_name"], c["customer_id"])
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(60)
        self.delivery_combo = QComboBox()
        self.delivery_combo.addItems(["Нет", "Да"])
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.discount_spin = QDoubleSpinBox()
        self.discount_spin.setRange(0, 100)
        self.discount_spin.setDecimals(2)
        self.discount_spin.setSuffix(" %")
        self.add_row("Покупатель", self.customer_combo)
        self.add_row("Описание", self.desc_edit)
        self.add_row("Доставка", self.delivery_combo)
        self.add_row("Время доставки", self.time_edit)
        self.add_row("Скидка", self.discount_spin)
        if data:
            idx = self.customer_combo.findData(data.get("customer_id"))
            if idx >= 0:
                self.customer_combo.setCurrentIndex(idx)
            self.desc_edit.setText(data.get("description") or "")
            self.set_yes_no(self.delivery_combo, data.get("delivery_needed"))
            if data.get("delivery_time"):
                self.time_edit.setTime(QTime.fromString(str(data["delivery_time"]), "HH:mm:ss"))
            self.discount_spin.setValue(float(data.get("discount") or 0))

    def get_data(self):
        return {
            "customer_id": self.customer_combo.currentData(),
            "description": self.desc_edit.toPlainText().strip(),
            "delivery_needed": self.delivery_combo.currentText() == "Да",
            "delivery_time": self.time_edit.time().toString("HH:mm:ss") if self.delivery_combo.currentText() == "Да" else None,
            "discount": self.discount_spin.value()
        }
