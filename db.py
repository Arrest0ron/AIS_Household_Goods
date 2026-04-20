import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from database.connection import DbConfig

log = logging.getLogger("db")


class Database:
    def __init__(self):
        self._conn = None

    def connect(self):
        if self._conn is None or self._conn.closed:
            cfg = DbConfig.from_env()
            log.info("Подключение к БД: %s@%s:%s/%s", cfg.user, cfg.host, cfg.port, cfg.dbname)
            self._conn = psycopg2.connect(
                host=cfg.host,
                port=cfg.port,
                dbname=cfg.dbname,
                user=cfg.user,
                password=cfg.password,
                cursor_factory=RealDictCursor,
                client_encoding="UTF8"
            )
            log.info("Подключение установлено")
        return self._conn

    def fetch_all(self, query, params=None):
        try:
            conn = self.connect()
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                result = cur.fetchall()
                log.debug("fetch_all: %s -> %d rows", query.strip()[:80], len(result))
                return result
        except Exception:
            log.exception("fetch_all FAILED: %s", query.strip()[:80])
            raise

    def fetch_one(self, query, params=None):
        try:
            conn = self.connect()
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                result = cur.fetchone()
                log.debug("fetch_one: %s -> %s", query.strip()[:80], "found" if result else "None")
                return result
        except Exception:
            log.exception("fetch_one FAILED: %s", query.strip()[:80])
            raise

    def execute(self, query, params=None, returning=False):
        try:
            conn = self.connect()
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                result = cur.fetchone() if returning else None
                conn.commit()
                log.debug("execute: %s -> OK", query.strip()[:80])
                return result
        except Exception:
            log.exception("execute FAILED: %s", query.strip()[:80])
            raise

    def execute_many(self, operations):
        try:
            conn = self.connect()
            with conn.cursor() as cur:
                result = None
                for query, params, ret in operations:
                    cur.execute(query, params or ())
                    if ret:
                        result = cur.fetchone()
                conn.commit()
                log.debug("execute_many: %d queries -> OK", len(operations))
                return result
        except Exception:
            log.exception("execute_many FAILED")
            raise

    def close(self):
        if self._conn and not self._conn.closed:
            self._conn.close()
            log.info("Соединение с БД закрыто")


db = Database()
