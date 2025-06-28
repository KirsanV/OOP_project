import unittest

from src.models import Vacancy


class TestVacancy(unittest.TestCase):
    def test_validate_salary_none(self) -> None:
        """
        Проверка, что при передаче salary=None значение salary устанавливается в 0.
        """
        vacancy: Vacancy = Vacancy(name="Test", url="http://example.com", salary=None, description="")
        self.assertEqual(vacancy.salary, 0)

    def test_validate_salary_empty_string(self) -> None:
        """
        Проверка, что при передаче salary="" значение salary устанавливается в 0.
        """
        vacancy: Vacancy = Vacancy(name="Test", url="http://example.com", salary="", description="")
        self.assertEqual(vacancy.salary, 0)

    def test_validate_salary_not_specified(self) -> None:
        """
        Проверка, что при передаче salary="не указана" значение salary устанавливается в 0.
        """
        vacancy: Vacancy = Vacancy(name="Test", url="http://example.com", salary="не указана", description="")
        self.assertEqual(vacancy.salary, 0)

    def test_validate_salary_string_number(self) -> None:
        """
        Проверка, что при передаче salary в виде строки с числом оно сохраняется как есть.
        """
        vacancy: Vacancy = Vacancy(name="Test", url="http://example.com", salary="50000", description="")
        self.assertEqual(vacancy.salary, "50000")

    def test_validate_salary_numeric(self) -> None:
        """
        Проверка, что при передаче salary как число оно сохраняется корректно.
        """
        vacancy: Vacancy = Vacancy(name="Test", url="http://example.com", salary=75000, description="")
        self.assertEqual(vacancy.salary, 75000)

    def test_validate_salary_float(self) -> None:
        """
        Проверка, что при передаче salary как float оно сохраняется корректно.
        """
        vacancy: Vacancy = Vacancy(name="Test", url="http://example.com", salary=12345.67, description="")
        self.assertEqual(vacancy.salary, 12345.67)

    def test_salary_value_with_string_digits(self) -> None:
        """
        Тест метода _salary_value() для строки с цифрами.
        """
        v1: Vacancy = Vacancy("name", "url", "100000", "")
        self.assertEqual(v1._salary_value(), 100000)

    def test_salary_value_with_non_digit_string(self) -> None:
        """
        Тест метода _salary_value() для строки без цифр.
        """
        v2: Vacancy = Vacancy("name", "url", "abcde", "")
        self.assertEqual(v2._salary_value(), 0)

    def test_comparison_lt_and_eq(self) -> None:
        """
        Тест сравнения вакансий по зарплате (< и ==).
        """
        v1: Vacancy = Vacancy("name1", "url1", 50000, "")
        v2: Vacancy = Vacancy("name2", "url2", 60000, "")
        v3: Vacancy = Vacancy("name3", "url3", 50000, "")

        self.assertTrue(v1 < v2)
        self.assertFalse(v2 < v1)
        self.assertTrue(v1 == v3)
        self.assertFalse(v1 == v2)

    def test_cast_to_object_list_basic(self) -> None:
        """
        Проверяет создание списка объектов вакансий из словарей с данными,
        правильность обработки зарплаты и отсутствия некоторых полей
        """
        data: list = [
            {
                'name': 'Vacancy 1',
                'alternate_url': 'http://vacancy1.com',
                'salary': {'from': 30000, 'to': 50000},
                'snippet': {'requirement': 'Some requirement'}
            },
            {
                'name': 'Vacancy 2',
                'alternate_url': 'http://vacancy2.com',
                'salary': {'from': None, 'to': None},
                'snippet': {'requirement': ''}
            }
        ]

        vacancies: list = Vacancy.cast_to_object_list(data)

        self.assertEqual(len(vacancies), 2)
        self.assertIsInstance(vacancies[0], Vacancy)
        self.assertEqual(vacancies[0].name, 'Vacancy 1')
        self.assertIn('http://vacancy1.com', vacancies[0].url)
        self.assertEqual(vacancies[0]._salary_value(), 30000)
        self.assertEqual(vacancies[1]._salary_value(), 0)

    def test_cast_to_object_list_with_missing_fields(self) -> None:
        """
        Проверяет создание объекта вакансии с отсутствующими ключами,
        ожидается присвоение имени(которое по умолчанию задано вот)
        """
        data: list = [
            {
                'alternate_url': 'http://example.com',
                'snippet': {}
            }
        ]

        vacancies: list = Vacancy.cast_to_object_list(data)

        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].name, 'Нет названия')
