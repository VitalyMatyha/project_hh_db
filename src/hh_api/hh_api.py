import requests

class HHAPI:
    """Работа с API hh.ru"""
    BASE_URL = "https://api.hh.ru"

    @staticmethod
    def get_employer_vacancies(employer_id: int, per_page: int = 20):
        """Возвращает вакансии компании"""
        url = f"{HHAPI.BASE_URL}/vacancies"
        params = {
            "employer_id": employer_id,
            "per_page": per_page
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
