from db import db


class CategoryRepository:
    def get_all(self):
        return db.fetch_all("SELECT * FROM categories ORDER BY category_id")

    def search(self, text):
        query = "SELECT * FROM categories WHERE category_name ILIKE %s ORDER BY category_id"
        return db.fetch_all(query, (f"%{text}%",))

    def get_by_id(self, category_id):
        return db.fetch_one("SELECT * FROM categories WHERE category_id = %s", (category_id,))

    def create(self, data):
        query = """
        INSERT INTO categories (category_name, adult_flag)
        VALUES (%s, %s)
        RETURNING category_id
        """
        return db.execute(query, (data["category_name"], data["adult_flag"]), returning=True)

    def update(self, category_id, data):
        query = """
        UPDATE categories
        SET category_name = %s, adult_flag = %s
        WHERE category_id = %s
        """
        db.execute(query, (data["category_name"], data["adult_flag"], category_id))

    def delete(self, category_id):
        db.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
