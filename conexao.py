import os
import mysql.connector
from mysql.connector import MySQLConnection
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


def conectar() -> MySQLConnection:
    return mysql.connector.connect(**DB_CONFIG)


class Query:
    def __init__(self, sql: str):
        self._sql = sql
        self._params: list = []

    def param(self, valor) -> "Query":
        self._params.append(valor)
        return self

    def params(self, *valores) -> "Query":
        self._params.extend(valores)
        return self

    def execute(self) -> list[dict]:
        conn = conectar()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(self._sql, self._params)
            if cursor.description:
                return cursor.fetchall()
            conn.commit()
            return []
        finally:
            cursor.close()
            conn.close()


def query(sql: str) -> Query:
    return Query(sql)
