import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from src.utils.config import DB_CONFIG

def create_database() -> None:
    """
    Создает базу данных, если её ещё нет.
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"]
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_CONFIG['dbname']}'")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f'CREATE DATABASE {DB_CONFIG["dbname"]}')
        print("База данных создана")
    cur.close()
    conn.close()


def create_tables() -> None:
    """
    Создает таблицы companies и vacancies, если их нет.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        company_id INTEGER PRIMARY KEY,
        company_name VARCHAR(255) NOT NULL,
        company_url TEXT
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vacancies (
        vacancy_id INTEGER PRIMARY KEY,
        vacancy_name VARCHAR(255) NOT NULL,
        salary_from INTEGER,
        salary_to INTEGER,
        currency VARCHAR(10),
        vacancy_url TEXT,
        company_id INTEGER REFERENCES companies(company_id)
    );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Таблицы созданы")
