class Session:
    current_user = None

    @classmethod
    def login(cls, user_data):
        cls.current_user = user_data

    @classmethod
    def logout(cls):
        cls.current_user = None

    @classmethod
    def is_admin(cls):
        return cls.current_user and cls.current_user.get("role") == "admin"

    @classmethod
    def is_user(cls):
        return cls.current_user and cls.current_user.get("role") == "user"
