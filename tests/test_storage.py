import json
import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from src.models import Vacancy
from src.storage import JSONVacancyStorage


@pytest.fixture
def temp_json_file() -> Generator[str, None, None]:
    """
    Создает временный файл для хранения данных вакансий.
    После теста удаляет файл
    """
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8') as tf:
        filename: str = tf.name
        yield filename
    os.remove(filename)


def test_get_all_vacancies_empty_file(temp_json_file: str) -> None:
    """
    Проверяет, что при пустом файле метод get_all_vacancies возвращает пустой список.
    """
    storage: JSONVacancyStorage = JSONVacancyStorage(filename=temp_json_file)
    vacancies: list = storage.get_all_vacancies()
    assert isinstance(vacancies, list)
    assert vacancies == []


def test_add_vacancy_and_get_all(temp_json_file: str) -> None:
    """
    Проверяет добавление вакансии и получение всех вакансий.
    """
    storage: JSONVacancyStorage = JSONVacancyStorage(filename=temp_json_file)
    vacancy: Vacancy = Vacancy(
        name='Test Vacancy',
        url='http://example.com',
        salary=50000,
        description='Test description'
    )

    storage.add_vacancy(vacancy)

    vacancies: list = storage.get_all_vacancies()
    assert len(vacancies) == 1
    v: Vacancy = vacancies[0]
    assert v.name == 'Test Vacancy'
    assert v.url == 'http://example.com'
    assert v.salary == 50000


def test_delete_vacancy(temp_json_file: str) -> None:
    """
    Проверяет удаление вакансии по URL.
    """
    storage: JSONVacancyStorage = JSONVacancyStorage(filename=temp_json_file)

    vacancy1: Vacancy = Vacancy(name='Vacancy 1', url='http://example.com/1', salary=30000, description='')
    vacancy2: Vacancy = Vacancy(name='Vacancy 2', url='http://example.com/2', salary=40000, description='')

    storage.add_vacancy(vacancy1)
    storage.add_vacancy(vacancy2)

    storage.delete_vacancy(vacancy1)

    vacancies: list = storage.get_all_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].url == 'http://example.com/2'


def test_get_all_vacancies_with_invalid_json(temp_json_file: str) -> None:
    """
    Проверяет обработку некорректного JSON в файле — должна возвращать пустой список.
     """
    with open(temp_json_file, 'w', encoding='utf-8') as f:
        f.write('Invalid JSON')

    storage: JSONVacancyStorage = JSONVacancyStorage(filename=temp_json_file)

    result: list = storage.get_all_vacancies()
    assert result == []


def test_save_to_file_creates_valid_json(tmp_path: Path) -> None:
    """
    Проверяет, что приватный метод _save_to_file создает валидный JSON-файл.
    """
    filename = tmp_path / "vacancies.json"

    storage = JSONVacancyStorage(filename=str(filename))

    vacancy = Vacancy(name='Test Save', url='http://save.com', salary=12345, description='desc')

    storage._save_to_file([vacancy])

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert data[0]['name'] == 'Test Save'
        assert data[0]['url'] == 'http://save.com'
        assert data[0]['salary'] == 12345
