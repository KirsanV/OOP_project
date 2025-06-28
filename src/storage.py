import json
import os
from abc import ABC, abstractmethod
from typing import List, Optional

from .models import Vacancy


class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в хранилище.
        """
        pass  # pragma: no cover

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из хранилища по URL.
        """
        pass  # pragma: no cover

    @abstractmethod
    def get_all_vacancies(self) -> List[Vacancy]:
        """
        Получает список всех вакансий из хранилища.
        """
        pass  # pragma: no cover


class JSONVacancyStorage(VacancyStorage):
    def __init__(self, filename: Optional[str] = None):
        if filename is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            filename = os.path.join(project_root, 'data', 'vacancies.json')
        self._filename = filename
        dir_name = os.path.dirname(self._filename)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в файл.
        """
        if self._is_duplicate(vacancy):
            return
        vacancies = self.get_all_vacancies()
        vacancies.append(vacancy)
        self._save_to_file(vacancies)

    def _is_duplicate(self, vacancy: Vacancy) -> bool:
        """
        Проверка на дубли
        """
        vacancies = self.get_all_vacancies()
        for v in vacancies:
            if v.url == vacancy.url:
                return True
        return False

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из файла по URL.
        """
        vacancies = self.get_all_vacancies()
        vacancies = [v for v in vacancies if v.url != vacancy.url]
        self._save_to_file(vacancies)

    def get_all_vacancies(self) -> List[Vacancy]:
        """
        Читает все вакансии из файла.
        """
        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
                return [self._dict_to_vacancy(d) for d in data_list]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def _save_to_file(self, vacancies: List[Vacancy]) -> None:
        """
        Сохраняет список вакансии в файл
        """
        dict_list = [self._vacancy_to_dict(v) for v in vacancies]
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(dict_list, f, ensure_ascii=False, indent=4)

    def _vacancy_to_dict(self, vacancy: Vacancy) -> dict:
        """
        Преобразует объект Vacancy в словарь для сохранения.
        """
        return {
            'name': vacancy.name,
            'url': vacancy.url,
            'salary': vacancy.salary,
            'description': vacancy.description,
        }

    def _dict_to_vacancy(self, data: dict) -> Vacancy:
        """
        Создает объект Vacancy из словаря данных.
        """

        return Vacancy(
            name=data.get('name', ''),
            url=data.get('url', ''),
            salary=data.get('salary'),
            description=data.get('description', '')
        )
