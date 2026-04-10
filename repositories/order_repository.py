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
        db.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))

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
        query = "INSERT INTO orderitems (order_id, item_id, amount) VALUES (%s, %s, %s) RETURNING position_id"
        return db.execute(query, (order_id, item_id, amount), returning=True)

    def update_item(self, position_id, amount):
        db.execute("UPDATE orderitems SET amount = %s WHERE position_id = %s", (amount, position_id))

    def delete_item(self, position_id):
        db.execute("DELETE FROM orderitems WHERE position_id = %s", (position_id,))

    def get_all_customers(self):
        return db.fetch_all("SELECT * FROM customers ORDER BY customer_name")

    def get_all_items(self):
        return db.fetch_all("SELECT * FROM items ORDER BY item_name")
