import requests
from typing import List, Dict

HH_BASE_URL = "https://api.hh.ru"


def get_employer_vacancies(employer_id: int, pages: int = 1) -> List[Dict]:
    """
    Получает вакансии конкретного работодателя с HH.ru.

    :param employer_id: ID работодателя на HH
    :param pages: количество страниц для запроса (по 100 вакансий на страницу)
    :return: список вакансий, каждая в виде словаря
    """
    vacancies: List[Dict] = []
    for page in range(pages):
        params = {"employer_id": employer_id, "page": page, "per_page": 100}
        response = requests.get(f"{HH_BASE_URL}/vacancies", params=params)
        if response.status_code != 200:
            continue
        data = response.json()
        for item in data.get("items", []):
            vacancies.append({
                "vacancy_id": int(item["id"]),
                "vacancy_name": item["name"],
                "salary_from": item["salary"]["from"] if item["salary"] else None,
                "salary_to": item["salary"]["to"] if item["salary"] else None,
                "currency": item["salary"]["currency"] if item["salary"] else None,
                "vacancy_url": item["alternate_url"],
                "company_id": int(item["employer"]["id"])
            })
    return vacancies
