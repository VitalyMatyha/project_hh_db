import pytest
from src.db.db_manager import DBManager

@pytest.fixture
def db():
    """Фикстура для подключения к БД и очистки после тестов"""
    db = DBManager()
    yield db
    db.close()

def test_get_companies_and_vacancies_count(db):
    result = db.get_companies_and_vacancies_count()
    assert isinstance(result, list)
    if result:
        assert isinstance(result[0][0], str)
        assert isinstance(result[0][1], int)

def test_get_all_vacancies(db):
    result = db.get_all_vacancies()
    assert isinstance(result, list)
    if result:
        assert len(result[0]) == 5  # company_name, vacancy_name, salary_from, salary_to, url

def test_get_avg_salary(db):
    avg = db.get_avg_salary()
    assert avg is None or isinstance(avg, float)

def test_get_vacancies_with_higher_salary(db):
    result = db.get_vacancies_with_higher_salary()
    assert isinstance(result, list)
    if result:
        assert isinstance(result[0][0], str)

def test_get_vacancies_with_keyword(db):
    keyword = "Python"
    result = db.get_vacancies_with_keyword(keyword)
    assert isinstance(result, list)
    if result:
        assert keyword.lower() in result[0][0].lower()
