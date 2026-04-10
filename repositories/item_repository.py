from db import db


class ItemRepository:
    def get_all(self):
        query = """
        SELECT i.*, c.category_name
        FROM items i
        LEFT JOIN categories c ON i.category_id = c.category_id
        ORDER BY i.item_id
        """
        return db.fetch_all(query)

    def search(self, text):
        query = """
        SELECT i.*, c.category_name
        FROM items i
        LEFT JOIN categories c ON i.category_id = c.category_id
        WHERE i.item_name ILIKE %s
        ORDER BY i.item_id
        """
        return db.fetch_all(query, (f"%{text}%",))

    def get_by_id(self, item_id):
        return db.fetch_one("SELECT * FROM items WHERE item_id = %s", (item_id,))

    def create(self, data):
        query = """
        INSERT INTO items (item_name, category_id, price, stock_quantity, mass)
        VALUES (%s, %s, %s, %s, %s) RETURNING item_id
        """
        return db.execute(query, (
            data["item_name"], data["category_id"], data["price"],
            data["stock_quantity"], data["mass"]
        ), returning=True)

    def update(self, item_id, data):
        query = """
        UPDATE items SET item_name = %s, category_id = %s, price = %s,
            stock_quantity = %s, mass = %s
        WHERE item_id = %s
        """
        db.execute(query, (
            data["item_name"], data["category_id"], data["price"],
            data["stock_quantity"], data["mass"], item_id
        ))

    def delete(self, item_id):
        db.execute("DELETE FROM items WHERE item_id = %s", (item_id,))

    def get_categories(self):
        return db.fetch_all("SELECT * FROM categories ORDER BY category_name")
