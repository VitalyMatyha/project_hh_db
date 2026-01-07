import psycopg2
from .config import DB_CONFIG
from typing import List, Dict, Optional

class DBManager:
    """Менеджер работы с базой hh_db"""

    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG, client_encoding='UTF8')

    def get_companies_and_vacancies_count(self) -> List[Dict]:
        """Список компаний и количество вакансий"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.employer_name, COUNT(v.vacancy_id)
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.employer_name;
            """)
            return [{"employer_name": row[0], "vacancies_count": row[1]} for row in cur.fetchall()]

    def get_all_vacancies(self) -> List[Dict]:
        """Список всех вакансий"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.employer_name, v.vacancy_name, v.salary_from, v.salary_to, v.currency, v.vacancy_url
                FROM vacancies v
                JOIN employers e ON e.employer_id = v.employer_id;
            """)
            return [
                {
                    "employer_name": row[0],
                    "vacancy_name": row[1],
                    "salary_from": row[2],
                    "salary_to": row[3],
                    "currency": row[4],
                    "vacancy_url": row[5]
                }
                for row in cur.fetchall()
            ]

    def get_avg_salary(self) -> Optional[float]:
        """Средняя зарплата"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((salary_from + salary_to)/2)
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
            """)
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Dict]:
        """Вакансии с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.employer_name, v.vacancy_name, v.salary_from, v.salary_to, v.currency, v.vacancy_url
                FROM vacancies v
                JOIN employers e ON e.employer_id = v.employer_id
                WHERE ((v.salary_from + v.salary_to)/2) > %s;
            """, (avg_salary,))
            return [
                {
                    "employer_name": row[0],
                    "vacancy_name": row[1],
                    "salary_from": row[2],
                    "salary_to": row[3],
                    "currency": row[4],
                    "vacancy_url": row[5]
                }
                for row in cur.fetchall()
            ]

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict]:
        """Вакансии по ключевому слову"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.employer_name, v.vacancy_name, v.salary_from, v.salary_to, v.currency, v.vacancy_url
                FROM vacancies v
                JOIN employers e ON e.employer_id = v.employer_id
                WHERE v.vacancy_name ILIKE %s;
            """, (f"%{keyword}%",))
            return [
                {
                    "employer_name": row[0],
                    "vacancy_name": row[1],
                    "salary_from": row[2],
                    "salary_to": row[3],
                    "currency": row[4],
                    "vacancy_url": row[5]
                }
                for row in cur.fetchall()
            ]
