import pytest
from unittest.mock import patch, MagicMock
from src.hh_api.hh_api import HHAPI

def test_get_employer_vacancies():
    mock_response = MagicMock()
    mock_response.json.return_value = {"items": [{"id": "1", "name": "Python Developer"}]}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        vacancies = HHAPI.get_employer_vacancies(employer_id=123)
        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"
