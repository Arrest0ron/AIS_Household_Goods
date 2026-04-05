import bcrypt
from repositories.auth_repository import AuthRepository


class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

    def login(self, login: str, password: str):
        user = self.repo.get_user_by_login(login)
        if not user:
            return None, "Пользователь не найден"
        if not user["is_active"]:
            return None, "Пользователь заблокирован"
        if not self.verify_password(password, user["password_hash"]):
            self.repo.add_login_history(user["user_id"], False)
            return None, "Неверный пароль"
        self.repo.add_login_history(user["user_id"], True)
        return user, None
