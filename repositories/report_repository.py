from db import db


class ReportRepository:
    def get_summary(self):
        data = {}
        data["categories_count"] = db.fetch_one("SELECT COUNT(*) as cnt FROM categories")["cnt"]
        data["items_count"] = db.fetch_one("SELECT COUNT(*) as cnt FROM items")["cnt"]
        data["customers_count"] = db.fetch_one("SELECT COUNT(*) as cnt FROM customers")["cnt"]
        data["orders_count"] = db.fetch_one("SELECT COUNT(*) as cnt FROM orders")["cnt"]
        data["supplies_count"] = db.fetch_one("SELECT COUNT(*) as cnt FROM supplies")["cnt"]
        data["total_stock"] = db.fetch_one("SELECT COALESCE(SUM(stock_quantity), 0) as s FROM items")["s"]
        data["total_stock_value"] = db.fetch_one("SELECT COALESCE(SUM(price * stock_quantity), 0) as s FROM items")["s"]
        return data

    def get_low_stock_items(self, threshold=10):
        query = """
        SELECT i.*, c.category_name
        FROM items i LEFT JOIN categories c ON i.category_id = c.category_id
        WHERE i.stock_quantity <= %s ORDER BY i.stock_quantity
        """
        return db.fetch_all(query, (threshold,))

    def get_category_summary(self):
        query = """
        SELECT c.category_name, COUNT(i.item_id) as item_count,
               COALESCE(SUM(i.stock_quantity), 0) as total_stock,
               COALESCE(SUM(i.price * i.stock_quantity), 0) as total_value
        FROM categories c LEFT JOIN items i ON c.category_id = i.category_id
        GROUP BY c.category_id, c.category_name ORDER BY c.category_name
        """
        return db.fetch_all(query)

    def get_order_summary(self):
        query = """
        SELECT o.order_id, c.customer_name, o.order_date, o.discount,
               COALESCE(SUM(oi.amount * i.price), 0) as total
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        LEFT JOIN orderitems oi ON o.order_id = oi.order_id
        LEFT JOIN items i ON oi.item_id = i.item_id
        GROUP BY o.order_id, c.customer_name, o.order_date, o.discount
        ORDER BY o.order_id
        """
        return db.fetch_all(query)

    def get_all_items(self):
        return db.fetch_all("""
            SELECT i.*, c.category_name
            FROM items i LEFT JOIN categories c ON i.category_id = c.category_id
            ORDER BY i.item_id
        """)

    def get_all_suppliers(self):
        return db.fetch_all("SELECT * FROM suppliers ORDER BY supplier_id")

    def get_all_customers(self):
        return db.fetch_all("SELECT * FROM customers ORDER BY customer_id")

    def get_supply_summary(self):
        query = """
        SELECT s.supply_id, sup.supplier_name, w.warehouse_address, s.supply_date,
               COALESCE(SUM(si.quantity), 0) as total_items,
               COUNT(si.item_id) as item_count
        FROM supplies s
        LEFT JOIN suppliers sup ON s.supplier_id = sup.supplier_id
        LEFT JOIN warehouses w ON s.warehouse_id = w.warehouse_id
        LEFT JOIN supplyitems si ON s.supply_id = si.supply_id
        GROUP BY s.supply_id, sup.supplier_name, w.warehouse_address, s.supply_date
        ORDER BY s.supply_id
        """
        return db.fetch_all(query)
