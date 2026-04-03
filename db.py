import psycopg2
from psycopg2.extras import RealDictCursor
from database.connection import DbConfig


class Database:
    def __init__(self):
        self._conn = None

    def connect(self):
        if self._conn is None or self._conn.closed:
            cfg = DbConfig.from_env()
            self._conn = psycopg2.connect(
                host=cfg.host,
                port=cfg.port,
                dbname=cfg.dbname,
                user=cfg.user,
                password=cfg.password,
                cursor_factory=RealDictCursor,
                client_encoding="UTF8"
            )
        return self._conn

    def fetch_all(self, query, params=None):
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()

    def fetch_one(self, query, params=None):
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchone()

    def execute(self, query, params=None, returning=False):
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            result = cur.fetchone() if returning else None
            conn.commit()
            return result

    def close(self):
        if self._conn and not self._conn.closed:
            self._conn.close()


db = Database()
