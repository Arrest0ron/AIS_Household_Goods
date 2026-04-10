from db import db


class WarehouseRepository:
    def get_all(self):
        return db.fetch_all("SELECT * FROM warehouses ORDER BY warehouse_id")

    def search(self, text):
        query = "SELECT * FROM warehouses WHERE warehouse_address ILIKE %s OR type ILIKE %s ORDER BY warehouse_id"
        return db.fetch_all(query, (f"%{text}%", f"%{text}%"))

    def get_by_id(self, warehouse_id):
        return db.fetch_one("SELECT * FROM warehouses WHERE warehouse_id = %s", (warehouse_id,))

    def create(self, data):
        query = """
        INSERT INTO warehouses (warehouse_address, capacity, type)
        VALUES (%s, %s, %s) RETURNING warehouse_id
        """
        return db.execute(query, (data["warehouse_address"], data["capacity"], data["type"]), returning=True)

    def update(self, warehouse_id, data):
        query = """
        UPDATE warehouses SET warehouse_address = %s, capacity = %s, type = %s WHERE warehouse_id = %s
        """
        db.execute(query, (data["warehouse_address"], data["capacity"], data["type"], warehouse_id))

    def delete(self, warehouse_id):
        db.execute("DELETE FROM warehouses WHERE warehouse_id = %s", (warehouse_id,))
