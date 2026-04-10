from db import db


class SupplierRepository:
    def get_all(self):
        return db.fetch_all("SELECT * FROM suppliers ORDER BY supplier_id")

    def search(self, text):
        query = "SELECT * FROM suppliers WHERE supplier_name ILIKE %s OR contact_info ILIKE %s ORDER BY supplier_id"
        return db.fetch_all(query, (f"%{text}%", f"%{text}%"))

    def get_by_id(self, supplier_id):
        return db.fetch_one("SELECT * FROM suppliers WHERE supplier_id = %s", (supplier_id,))

    def create(self, data):
        query = "INSERT INTO suppliers (supplier_name, contact_info) VALUES (%s, %s) RETURNING supplier_id"
        return db.execute(query, (data["supplier_name"], data["contact_info"]), returning=True)

    def update(self, supplier_id, data):
        db.execute("UPDATE suppliers SET supplier_name = %s, contact_info = %s WHERE supplier_id = %s",
                    (data["supplier_name"], data["contact_info"], supplier_id))

    def delete(self, supplier_id):
        db.execute("DELETE FROM suppliers WHERE supplier_id = %s", (supplier_id,))
