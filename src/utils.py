from typing import List, Optional

from .models import Vacancy


def filter_vacancies(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """
    Фильтрует список вакансий по ключевым словам, которые должны присутствовать в названии или описании
    """
    filtered: List[Vacancy] = []
    for v in vacancies:
        text_combined = (v.name + ' ' + v.description).lower()
        if all(keyword.lower() in text_combined for keyword in keywords):
            filtered.append(v)
    return filtered


def get_top_n_vacancies(vacancies: List[Vacancy], n: int) -> List[Vacancy]:
    """
    Возвращает топ N вакансий, отсортированных по убыванию
    """
    sorted_list = sorted(vacancies, reverse=True)
    return sorted_list[:n]


def get_vacancies_by_salary(
    vacancies: List[Vacancy],
    min_salary: Optional[float] = None,
    max_salary: Optional[float] = None
) -> List[Vacancy]:
    """
    Фильтрует вакансии по диапазону зарплат
    """
    result: List[Vacancy] = []
    for v in vacancies:
        val = v._salary_value()
        if min_salary is not None and val < min_salary:
            continue
        if max_salary is not None and val > max_salary:
            continue
        result.append(v)
    return result


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Выводит информацию о вакансиях в консоль
    """
    for v in vacancies:
        print(f"Название: {v.name}")
        print(f"Ссылка: {v.url}")
        print(f"Зарплата: {v.salary}")
        print(f"Описание/Требования: {v.description}")
        print("-" * 40)
