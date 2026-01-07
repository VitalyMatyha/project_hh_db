from unittest.mock import patch
from src.api.hh_api import get_employer_vacancies

def mock_hh_response(*args, **kwargs):
    return {
        "items": [
            {
                "id": "123",
                "name": "Python Developer",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "alternate_url": "http://hh.ru/vacancy/123",
                "employer": {"id": 1}
            }
        ]
    }

@patch("requests.get")
def test_get_employer_vacancies(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = mock_hh_response

    vacancies = get_employer_vacancies(1, pages=1)
    assert isinstance(vacancies, list)
    assert vacancies[0]["vacancy_id"] == 123
    assert vacancies[0]["vacancy_name"] == "Python Developer"
    assert vacancies[0]["salary_from"] == 100000
    assert vacancies[0]["salary_to"] == 150000
    assert vacancies[0]["currency"] == "RUR"
    assert vacancies[0]["vacancy_url"] == "http://hh.ru/vacancy/123"
    assert vacancies[0]["company_id"] == 1
