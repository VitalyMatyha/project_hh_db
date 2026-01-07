from db.db_create import create_database
from db.db_tables import create_tables

def main():
    try:
        create_database()
    except Exception as e:
        print(f"Ошибка при создании базы: {e}")

    try:
        create_tables()
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")

    print("Проект готов к использованию!")

if __name__ == "__main__":
    main()
