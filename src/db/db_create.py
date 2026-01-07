import psycopg2
from psycopg2 import sql
from .config import DB_CONFIG

def create_database():
    """Создаёт базу hh_db, если не существует"""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            client_encoding='UTF8'
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_CONFIG["dbname"])))
        print(f"База данных {DB_CONFIG['dbname']} успешно создана")
        cur.close()
        conn.close()
    except psycopg2.errors.DuplicateDatabase:
        print(f"База данных {DB_CONFIG['dbname']} уже существует")
    except Exception as e:
        print(f"Ошибка при создании базы: {e}")
