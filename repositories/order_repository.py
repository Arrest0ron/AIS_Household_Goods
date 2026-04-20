from db import db


class OrderRepository:
    def get_all(self):
        query = """
        SELECT o.*, c.customer_name
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        ORDER BY o.order_id
        """
        return db.fetch_all(query)

    def get_by_id(self, order_id):
        return db.fetch_one("SELECT * FROM orders WHERE order_id = %s", (order_id,))

    def create(self, data):
        query = """
        INSERT INTO orders (customer_id, description, delivery_needed, delivery_time, discount)
        VALUES (%s, %s, %s, %s, %s) RETURNING order_id
        """
        return db.execute(query, (
            data["customer_id"], data["description"],
            data["delivery_needed"], data["delivery_time"], data["discount"]
        ), returning=True)

    def update(self, order_id, data):
        query = """
        UPDATE orders SET customer_id = %s, description = %s,
            delivery_needed = %s, delivery_time = %s, discount = %s
        WHERE order_id = %s
        """
        db.execute(query, (
            data["customer_id"], data["description"],
            data["delivery_needed"], data["delivery_time"], data["discount"],
            order_id
        ))

    def delete(self, order_id):
        items = self.get_items(order_id)
        ops = []
        for it in items:
            ops.append(("UPDATE items SET stock_quantity = stock_quantity + %s WHERE item_id = %s",
                        (it["amount"], it["item_id"]), False))
        ops.append(("DELETE FROM orders WHERE order_id = %s", (order_id,), False))
        db.execute_many(ops)

    def get_items(self, order_id):
        query = """
        SELECT oi.*, i.item_name, i.price
        FROM orderitems oi
        LEFT JOIN items i ON oi.item_id = i.item_id
        WHERE oi.order_id = %s
        ORDER BY oi.position_id
        """
        return db.fetch_all(query, (order_id,))

    def add_item(self, order_id, item_id, amount):
        return db.execute_many([
            ("INSERT INTO orderitems (order_id, item_id, amount) VALUES (%s, %s, %s) RETURNING position_id",
             (order_id, item_id, amount), True),
            ("UPDATE items SET stock_quantity = stock_quantity - %s WHERE item_id = %s",
             (amount, item_id), False),
        ])

    def update_item(self, position_id, amount):
        old = db.fetch_one("SELECT item_id, amount FROM orderitems WHERE position_id = %s", (position_id,))
        if old:
            delta = amount - old["amount"]
            db.execute_many([
                ("UPDATE orderitems SET amount = %s WHERE position_id = %s", (amount, position_id), False),
                ("UPDATE items SET stock_quantity = stock_quantity - %s WHERE item_id = %s",
                 (delta, old["item_id"]), False),
            ])

    def delete_item(self, position_id):
        old = db.fetch_one("SELECT item_id, amount FROM orderitems WHERE position_id = %s", (position_id,))
        if old:
            db.execute_many([
                ("DELETE FROM orderitems WHERE position_id = %s", (position_id,), False),
                ("UPDATE items SET stock_quantity = stock_quantity + %s WHERE item_id = %s",
                 (old["amount"], old["item_id"]), False),
            ])

    def get_order_detail(self, order_id):
        query = """
        SELECT o.*, c.customer_name, c.phone, c.email
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.order_id = %s
        """
        return db.fetch_one(query, (order_id,))

    def search(self, text):
        query = """
        SELECT o.*, c.customer_name
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        WHERE c.customer_name ILIKE %s OR o.description ILIKE %s
        ORDER BY o.order_id
        """
        pattern = f"%{text}%"
        return db.fetch_all(query, (pattern, pattern))

    def search_by_date_range(self, start_date, end_date):
        query = """
        SELECT o.*, c.customer_name
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.order_date >= %s AND o.order_date <= %s
        ORDER BY o.order_id
        """
        return db.fetch_all(query, (start_date, end_date))

    def search_combined(self, text, start_date, end_date):
        query = """
        SELECT o.*, c.customer_name
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        WHERE (c.customer_name ILIKE %s OR o.description ILIKE %s)
          AND o.order_date >= %s AND o.order_date <= %s
        ORDER BY o.order_id
        """
        pattern = f"%{text}%"
        return db.fetch_all(query, (pattern, pattern, start_date, end_date))


