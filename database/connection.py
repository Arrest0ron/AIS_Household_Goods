import os
import psycopg2
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


class DatabaseManager:
    def __init__(self, config: DbConfig | None = None):
        self.config = config or DbConfig.from_env()
        self.conn = None

    def connect(self) -> str:
        try:
            self.conn = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                dbname=self.config.dbname,
                user=self.config.user,
                password=self.config.password,
            )
            return self._get_version()
        except psycopg2.Error as e:
            raise ConnectionError(f"Ошибка подключения: {e}")

    def _get_version(self) -> str:
        with self.conn.cursor() as cur:
            cur.execute("SELECT version()")
            return cur.fetchone()[0]

    def get_tables(self) -> list[str]:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            return [row[0] for row in cur.fetchall()]

    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
