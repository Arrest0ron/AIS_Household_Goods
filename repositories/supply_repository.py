from db import db


class SupplyRepository:
    def get_all(self):
        query = """
        SELECT s.*, sup.supplier_name, w.warehouse_address
        FROM supplies s
        LEFT JOIN suppliers sup ON s.supplier_id = sup.supplier_id
        LEFT JOIN warehouses w ON s.warehouse_id = w.warehouse_id
        ORDER BY s.supply_id
        """
        return db.fetch_all(query)

    def get_by_id(self, supply_id):
        return db.fetch_one("SELECT * FROM supplies WHERE supply_id = %s", (supply_id,))

    def create(self, data):
        query = "INSERT INTO supplies (supplier_id, warehouse_id, supply_date) VALUES (%s, %s, %s) RETURNING supply_id"
        return db.execute(query, (data["supplier_id"], data["warehouse_id"], data["supply_date"]), returning=True)

    def update(self, supply_id, data):
        db.execute("UPDATE supplies SET supplier_id = %s, warehouse_id = %s, supply_date = %s WHERE supply_id = %s",
                    (data["supplier_id"], data["warehouse_id"], data["supply_date"], supply_id))

    def delete(self, supply_id):
        items = self.get_items(supply_id)
        ops = []
        for it in items:
            ops.append(("UPDATE items SET stock_quantity = stock_quantity - %s WHERE item_id = %s",
                        (it["quantity"], it["item_id"]), False))
        ops.append(("DELETE FROM supplies WHERE supply_id = %s", (supply_id,), False))
        db.execute_many(ops)

    def get_items(self, supply_id):
        query = """
        SELECT si.*, i.item_name
        FROM supplyitems si
        LEFT JOIN items i ON si.item_id = i.item_id
        WHERE si.supply_id = %s
        ORDER BY si.income_id
        """
        return db.fetch_all(query, (supply_id,))

    def get_items_with_prices(self, supply_id):
        query = """
        SELECT si.*, i.item_name, i.price
        FROM supplyitems si
        LEFT JOIN items i ON si.item_id = i.item_id
        WHERE si.supply_id = %s
        ORDER BY si.income_id
        """
        return db.fetch_all(query, (supply_id,))

    def get_supply_detail(self, supply_id):
        query = """
        SELECT s.*, sup.supplier_name, sup.contact_info,
               w.warehouse_address
        FROM supplies s
        LEFT JOIN suppliers sup ON s.supplier_id = sup.supplier_id
        LEFT JOIN warehouses w ON s.warehouse_id = w.warehouse_id
        WHERE s.supply_id = %s
        """
        return db.fetch_one(query, (supply_id,))

    def add_item(self, supply_id, item_id, quantity):
        return db.execute_many([
            ("INSERT INTO supplyitems (supply_id, item_id, quantity) VALUES (%s, %s, %s) RETURNING income_id",
             (supply_id, item_id, quantity), True),
            ("UPDATE items SET stock_quantity = stock_quantity + %s WHERE item_id = %s",
             (quantity, item_id), False),
        ])

    def update_item(self, income_id, quantity):
        old = db.fetch_one("SELECT item_id, quantity FROM supplyitems WHERE income_id = %s", (income_id,))
        if old:
            delta = quantity - old["quantity"]
            db.execute_many([
                ("UPDATE supplyitems SET quantity = %s WHERE income_id = %s", (quantity, income_id), False),
                ("UPDATE items SET stock_quantity = stock_quantity + %s WHERE item_id = %s",
                 (delta, old["item_id"]), False),
            ])

    def delete_item(self, income_id):
        old = db.fetch_one("SELECT item_id, quantity FROM supplyitems WHERE income_id = %s", (income_id,))
        if old:
            db.execute_many([
                ("DELETE FROM supplyitems WHERE income_id = %s", (income_id,), False),
                ("UPDATE items SET stock_quantity = stock_quantity - %s WHERE item_id = %s",
                 (old["quantity"], old["item_id"]), False),
            ])

    def get_all_suppliers(self):
        return db.fetch_all("SELECT * FROM suppliers ORDER BY supplier_name")

    def get_all_warehouses(self):
        return db.fetch_all("SELECT * FROM warehouses ORDER BY warehouse_address")

    def get_all_items(self):
        return db.fetch_all("SELECT * FROM items ORDER BY item_name")

    def search(self, text):
        query = """
        SELECT s.*, sup.supplier_name, w.warehouse_address
        FROM supplies s
        LEFT JOIN suppliers sup ON s.supplier_id = sup.supplier_id
        LEFT JOIN warehouses w ON s.warehouse_id = w.warehouse_id
        WHERE sup.supplier_name ILIKE %s OR w.warehouse_address ILIKE %s
        ORDER BY s.supply_id
        """
        pattern = f"%{text}%"
        return db.fetch_all(query, (pattern, pattern))

    def search_by_date_range(self, start_date, end_date):
        query = """
        SELECT s.*, sup.supplier_name, w.warehouse_address
        FROM supplies s
        LEFT JOIN suppliers sup ON s.supplier_id = sup.supplier_id
        LEFT JOIN warehouses w ON s.warehouse_id = w.warehouse_id
        WHERE s.supply_date >= %s AND s.supply_date <= %s
        ORDER BY s.supply_id
        """
        return db.fetch_all(query, (start_date, end_date))

    def search_combined(self, text, start_date, end_date):
        query = """
        SELECT s.*, sup.supplier_name, w.warehouse_address
        FROM supplies s
        LEFT JOIN suppliers sup ON s.supplier_id = sup.supplier_id
        LEFT JOIN warehouses w ON s.warehouse_id = w.warehouse_id
        WHERE (sup.supplier_name ILIKE %s OR w.warehouse_address ILIKE %s)
          AND s.supply_date >= %s AND s.supply_date <= %s
        ORDER BY s.supply_id
        """
        pattern = f"%{text}%"
        return db.fetch_all(query, (pattern, pattern, start_date, end_date))
