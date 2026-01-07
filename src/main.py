from src.db.db_create import create_database, create_tables
from src.db.db_manager import DBManager
from src.api.hh_api import get_employer_vacancies
import psycopg2

def main():
    # 1. Создаем базу и таблицы
    create_database()
    create_tables()
    db = DBManager()

    # 2. Список компаний (10 компаний с их employer_id на HH)
    companies_list = [
        {"id": 1582, "name": "Яндекс"},
        {"id": 1324, "name": "Mail.ru Group"},
        {"id": 1111, "name": "SberTech"},
        {"id": 2222, "name": "VK"},
        {"id": 3333, "name": "Tinkoff"},
        {"id": 4444, "name": "Ozon"},
        {"id": 5555, "name": "Alfa-Bank"},
        {"id": 6666, "name": "Luxoft"},
        {"id": 7777, "name": "EPAM"},
        {"id": 8888, "name": "Rambler"}
    ]

    # 3. Добавляем компании и вакансии
    for comp in companies_list:
        db.cur.execute(
            "INSERT INTO companies (company_id, company_name) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (comp["id"], comp["name"])
        )
        vacancies = get_employer_vacancies(comp["id"], pages=1)
        for vac in vacancies:
            db.cur.execute("""
                INSERT INTO vacancies (vacancy_id, vacancy_name, salary_from, salary_to, currency, vacancy_url, company_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
            """, (
                vac["vacancy_id"], vac["vacancy_name"], vac["salary_from"],
                vac["salary_to"], vac["currency"], vac["vacancy_url"], vac["company_id"]
            ))
    db.conn.commit()

    # 4. Демонстрация методов DBManager
    print("Компании и количество вакансий:")
    for company, count in db.get_companies_and_vacancies_count():
        print(f"{company}: {count} вакансий")

    print("\nСредняя зарплата по вакансиям:", db.get_avg_salary())

    print("\nВакансии с зарплатой выше средней:")
    for vac, in db.get_vacancies_with_higher_salary():
        print(vac)

    keyword = "Python"
    print(f"\nВакансии с ключевым словом '{keyword}':")
    for vac, in db.get_vacancies_with_keyword(keyword):
        print(vac)

    db.close()


if __name__ == "__main__":
    main()
