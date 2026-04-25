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
        db.execute("DELETE FROM supplies WHERE supply_id = %s", (supply_id,))

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
        query = "INSERT INTO supplyitems (supply_id, item_id, quantity) VALUES (%s, %s, %s) RETURNING income_id"
        return db.execute(query, (supply_id, item_id, quantity), returning=True)

    def update_item(self, income_id, quantity):
        db.execute("UPDATE supplyitems SET quantity = %s WHERE income_id = %s", (quantity, income_id))

    def delete_item(self, income_id):
        db.execute("DELETE FROM supplyitems WHERE income_id = %s", (income_id,))

    def get_all_suppliers(self):
        return db.fetch_all("SELECT * FROM suppliers ORDER BY supplier_name")

    def get_all_warehouses(self):
        return db.fetch_all("SELECT * FROM warehouses ORDER BY warehouse_address")

    def get_all_items(self):
        return db.fetch_all("SELECT * FROM items ORDER BY item_name")
