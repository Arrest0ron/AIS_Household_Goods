from db import db


class CustomerRepository:
    def get_all(self):
        return db.fetch_all("SELECT * FROM customers ORDER BY customer_id")

    def search(self, text):
        query = "SELECT * FROM customers WHERE customer_name ILIKE %s OR phone ILIKE %s OR email ILIKE %s ORDER BY customer_id"
        return db.fetch_all(query, (f"%{text}%", f"%{text}%", f"%{text}%"))

    def get_by_id(self, customer_id):
        return db.fetch_one("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))

    def create(self, data):
        query = "INSERT INTO customers (customer_name, phone, email) VALUES (%s, %s, %s) RETURNING customer_id"
        return db.execute(query, (data["customer_name"], data["phone"], data["email"]), returning=True)

    def update(self, customer_id, data):
        db.execute("UPDATE customers SET customer_name = %s, phone = %s, email = %s WHERE customer_id = %s",
                    (data["customer_name"], data["phone"], data["email"], customer_id))

    def delete(self, customer_id):
        db.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
