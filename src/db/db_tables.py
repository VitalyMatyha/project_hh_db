import psycopg2
from .config import DB_CONFIG

def create_tables():
    """Создаёт таблицы employers и vacancies"""
    try:
        conn = psycopg2.connect(**DB_CONFIG, client_encoding='UTF8')
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id SERIAL PRIMARY KEY,
                employer_name VARCHAR(255) NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR(255) NOT NULL,
                salary_from NUMERIC,
                salary_to NUMERIC,
                currency VARCHAR(10),
                vacancy_url TEXT,
                employer_id INTEGER REFERENCES employers(employer_id)
            );
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("Таблицы успешно созданы")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
