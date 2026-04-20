from db import db


class AuthRepository:
    def get_user_by_login(self, login):
        query = """
        SELECT user_id, login, password_hash, role, is_active, customer_id
        FROM users
        WHERE login = %s
        """
        return db.fetch_one(query, (login,))

    def add_login_history(self, user_id, is_success):
        query = """
        INSERT INTO login_history (user_id, is_success)
        VALUES (%s, %s)
        """
        db.execute(query, (user_id, is_success))
