from typing import List, Optional, Union


class Vacancy:
    """
    Класс для представления вакансии
    """

    __slots__ = ['name', 'url', 'salary', 'description']

    def __init__(self, name: str, url: str, salary: Optional[Union[str, int, float]] = None, description: str = ""):
        """
        Инициализация объекта вакансии

        """
        self.name = name
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    def _validate_salary(self, salary: Optional[object]) -> object:
        """
        Валидирует и преобразует значение зарплаты
        """
        if salary is None:
            return 0
        if isinstance(salary, str):
            if salary.strip() == "" or salary.lower() == "не указана":
                return 0
            return salary
        elif isinstance(salary, (int, float)):
            return salary
        else:
            return 0

    def __lt__(self, other: 'Vacancy') -> bool:
        """
        Меньше чем — сравнение по зарплате
        """
        return self._salary_value() < other._salary_value()

    def __eq__(self, other: object) -> bool:
        """
        Сравнение по зарплате
        """
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._salary_value() == other._salary_value()

    def _salary_value(self) -> int:
        """
        Получает числовое значение зарплаты для сравнения
        """

        if isinstance(self.salary, (int, float)):
            return int(self.salary)

        if isinstance(self.salary, str):
            import re
            numbers = re.findall(r'\d+', self.salary)
            if numbers:
                return int(numbers[0])

        return 0

    @staticmethod
    def cast_to_object_list(vacancies_data: List[dict]) -> List['Vacancy']:
        """
        Преобразует список словарей с данными о вакансиях в список объектов Vacancy

        """
        result: List[Vacancy] = []

        for item in vacancies_data:
            name = item.get('name', 'Нет названия')
            url = item.get('alternate_url', '')

            salary_info = item.get('salary')
            if salary_info:
                from_salary = salary_info.get('from')
                to_salary = salary_info.get('to')
                if from_salary and to_salary:
                    salary_str = f"{from_salary} - {to_salary} руб."
                elif from_salary:
                    salary_str = f"от {from_salary} руб."
                elif to_salary:
                    salary_str = f"до {to_salary} руб."
                else:
                    salary_str = None
            else:
                salary_str = None

            description = item.get('snippet', {}).get('requirement', '') or ''

            vacancy_obj = Vacancy(
                name=name,
                url=url,
                salary=salary_str,
                description=description
            )
            result.append(vacancy_obj)

        return result
