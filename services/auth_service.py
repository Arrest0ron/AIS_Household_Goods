import logging
import bcrypt
from repositories.auth_repository import AuthRepository

log = logging.getLogger("auth")


class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

    def login(self, login: str, password: str):
        log.info("Попытка входа: login=%s", login)
        try:
            user = self.repo.get_user_by_login(login)
        except Exception:
            log.exception("Ошибка БД при поиске пользователя: %s", login)
            return None, "Ошибка подключения к базе данных"
        if not user:
            log.warning("Пользователь не найден: %s", login)
            return None, "Пользователь не найден"
        if not user["is_active"]:
            log.warning("Пользователь заблокирован: %s", login)
            return None, "Пользователь заблокирован"
        if not self.verify_password(password, user["password_hash"]):
            log.warning("Неверный пароль: %s", login)
            self.repo.add_login_history(user["user_id"], False)
            return None, "Неверный пароль"
        self.repo.add_login_history(user["user_id"], True)
        log.info("Успешный вход: login=%s, role=%s", login, user["role"])
        return user, None
