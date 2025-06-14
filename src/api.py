import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Union

import requests


class VacancyAPI(ABC):
    """
    Абстрактный класс для работы с API вакансий.
    Определяет интерфейс для получения вакансий по поисковому запросу
    """
    @abstractmethod
    def _connect(self) -> None:
        """
        Устанавливает соединение с API
        """
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict]:
        """
        Получает список вакансий по заданному поисковому запросу

        """
        pass


logger = logging.getLogger(__name__)


class HeadHunterAPI(VacancyAPI):
    """
    Реализация API для hh.ru
    Позволяет получать вакансии с сайта HeadHunter по поисковому запросу
    """

    __BASE_URL = 'https://api.hh.ru/vacancies'

    def __init__(self) -> None:
        self.__session = requests.Session()
        self._connected = False

    def _connect(self) -> None:
        """
        Реализация абстрактного метода подключения к API.
        """
        if not self._connected:
            response = self.__session.get(self.__BASE_URL)
            if response.status_code == 200:
                self._connected = True
            else:
                raise ConnectionError(f"Ошибка подключения к {self.__BASE_URL}, статус: {response.status_code}")

    def get_vacancies(self, keyword: str) -> List[Dict]:
        """
        Получает вакансии по ключевому слову.
        """
        self._connect()
        params: Dict[str, Union[str, int]] = {
            'text': keyword,
            'per_page': 10
        }
        response = self.__session.get(self.__BASE_URL, params=params)
        if response.status_code != 200:
            raise ConnectionError(f"Ошибка получения данных: {response.status_code}")

        data = response.json()
        items = data.get('items', [])

        vacancies_list = []
        for item in items:
            vacancy_data = {
                'name': item.get('name', ''),
                'alternate_url': item.get('alternate_url', ''),
                'salary': item.get('salary'),
                'snippet': {
                    'requirement': item.get('snippet', {}).get('requirement', '')
                }
            }
            vacancies_list.append(vacancy_data)

        return vacancies_list
