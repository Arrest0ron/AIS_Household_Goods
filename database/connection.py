import os
from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str = "localhost"
    port: int = 5432
    dbname: str = "ais_shop_db"
    user: str = "ais_admin"
    password: str = "ais_admin_pass"

    @classmethod
    def from_env(cls):
        return cls(
            host=os.getenv("PG_HOST", "localhost"),
            port=int(os.getenv("PG_PORT", "5432")),
            dbname=os.getenv("PG_DB", "ais_shop_db"),
            user=os.getenv("PG_USER", "ais_admin"),
            password=os.getenv("PG_PASS", "ais_admin_pass"),
        )
