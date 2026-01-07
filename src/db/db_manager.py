import psycopg2
from typing import List, Tuple
from src.utils.config import DB_CONFIG


class DBManager:
    """
    Класс для работы с базой данных HH: компании и вакансии.
    """

    def __init__(self) -> None:
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Возвращает список компаний и количество вакансий в каждой.

        :return: список кортежей (название компании, количество вакансий)
        """
        self.cur.execute("""
            SELECT c.company_name, COUNT(v.vacancy_id)
            FROM companies c
            LEFT JOIN vacancies v ON c.company_id = v.company_id
            GROUP BY c.company_name;
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, int, int, str]]:
        """
        Возвращает все вакансии с информацией о компании, зарплате и ссылке.

        :return: список кортежей (название компании, вакансия, salary_from, salary_to, url)
        """
        self.cur.execute("""
            SELECT c.company_name, v.vacancy_name, v.salary_from, v.salary_to, v.vacancy_url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.company_id;
        """)
        return self.cur.fetchall()

    def get_avg_salary(self) -> float:
        """
        Вычисляет среднюю зарплату по вакансиям, где зарплата указана.

        :return: средняя зарплата
        """
        self.cur.execute("""
            SELECT AVG((salary_from + salary_to) / 2)
            FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
        """)
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str]]:
        """
        Возвращает вакансии с зарплатой выше средней.

        :return: список кортежей (название вакансии)
        """
        self.cur.execute("""
            SELECT vacancy_name
            FROM vacancies
            WHERE (salary_from + salary_to) / 2 >
                  (SELECT AVG((salary_from + salary_to) / 2) FROM vacancies
                   WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL);
        """)
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str]]:
        """
        Возвращает вакансии, в названии которых содержится keyword.

        :param keyword: ключевое слово для поиска
        :return: список кортежей (название вакансии)
        """
        self.cur.execute("""
            SELECT vacancy_name
            FROM vacancies
            WHERE vacancy_name ILIKE %s;
        """, (f"%{keyword}%",))
        return self.cur.fetchall()

    def close(self) -> None:
        """Закрывает соединение с БД."""
        self.cur.close()
        self.conn.close()
