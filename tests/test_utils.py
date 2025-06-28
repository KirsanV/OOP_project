import pytest
from pytest import CaptureFixture

from src.models import Vacancy
from src.utils import filter_vacancies, get_top_n_vacancies, get_vacancies_by_salary, print_vacancies


@pytest.fixture
def sample_vacancies() -> list[Vacancy]:
    """
    Создает список фиктивных вакансий для тестирования.
    """
    v1: Vacancy = Vacancy(
        name='Python Developer',
        url='http://example.com/1',
        salary=60000,
        description='Looking for a Python developer with Django experience'
    )
    v2: Vacancy = Vacancy(
        name='Java Developer',
        url='http://example.com/2',
        salary=70000,
        description='Java backend developer needed'
    )
    v3: Vacancy = Vacancy(
        name='Data Scientist',
        url='http://example.com/3',
        salary=80000,
        description='Experience with machine learning and Python'
    )
    return [v1, v2, v3]


def test_filter_vacancies_keywords(sample_vacancies: list[Vacancy]) -> None:
    """
    Тестирует фильтрацию вакансий по ключевым словам.
    """
    keywords: list[str] = ['Python', 'developer']
    filtered: list[Vacancy] = filter_vacancies(sample_vacancies, keywords)

    assert len(filtered) == 1
    assert filtered[0].name == 'Python Developer'


def test_filter_vacancies_case_insensitive(sample_vacancies: list[Vacancy]) -> None:
    """
    Проверяет нечувствительность к регистру при фильтрации.
    """
    keywords: list[str] = ['python']
    filtered: list[Vacancy] = filter_vacancies(sample_vacancies, keywords)

    assert len(filtered) == 2


def test_get_top_n_vacancies(sample_vacancies: list[Vacancy]) -> None:
    """
    Тестирует получение топ-N вакансий по убыванию (по зарплате).
    """
    top_2: list[Vacancy] = get_top_n_vacancies(sample_vacancies, 2)

    salaries = [v._salary_value() for v in top_2]

    assert salaries == sorted(salaries, reverse=True)


def test_get_vacancies_by_salary_min_max(sample_vacancies: list[Vacancy]) -> None:
    """
    Тестирует фильтрацию вакансий по диапазону зарплат.
    """
    result_min: list[Vacancy] = get_vacancies_by_salary(sample_vacancies, min_salary=75000)
    assert all(v._salary_value() >= 75000 for v in result_min)

    result_max: list[Vacancy] = get_vacancies_by_salary(sample_vacancies, max_salary=65000)
    assert all(v._salary_value() <= 65000 for v in result_max)

    result_range: list[Vacancy] = get_vacancies_by_salary(
        sample_vacancies, min_salary=65000, max_salary=80000)
    for v in result_range:
        assert 65000 <= v._salary_value() <= 80000


def test_print_vacancies(capsys: CaptureFixture, sample_vacancies: list[Vacancy]) -> None:
    """
    Тестирует вывод информации о вакансиях в консоль.
    """
    print_vacancies(sample_vacancies)

    captured = capsys.readouterr()

    for v in sample_vacancies:
        assert v.name in captured.out
        assert v.url in captured.out
        assert str(v.salary) in captured.out
        assert v.description in captured.out
