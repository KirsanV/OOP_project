import unittest
from unittest.mock import MagicMock, patch

from src.api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    """
    Тестовый класс для проверки работы класса HeadHunterAPI
    """

    @patch('src.api.requests.Session')
    def test_connect_success(self, mock_session_class: 'MagicMock') -> None:
        """
        Тест успешного подключения к API.
        """
        mock_session = mock_session_class.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response

        api = HeadHunterAPI()
        api._connected = False
        api._connect()

        self.assertTrue(api._connected)
        mock_session.get.assert_called_with('https://api.hh.ru/vacancies')

    @patch('src.api.requests.Session')
    def test_connect_failure(self, mock_session_class: 'MagicMock') -> None:
        """
        Тест обработки ошибки при неуспешном подключении
        """
        mock_session = mock_session_class.return_value
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_session.get.return_value = mock_response

        api = HeadHunterAPI()
        with self.assertRaises(ConnectionError):
            api._connect()

    @patch('src.api.requests.Session')
    def test_get_vacancies_success(self, mock_session_class: 'MagicMock') -> None:
        """
        Тест успешного получения вакансий
        """
        mock_session = mock_session_class.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'items': [
                {
                    'name': 'Test Vacancy',
                    'alternate_url': 'https://example.com/vacancy/1',
                    'salary': {'from': 1000, 'to': 2000},
                    'snippet': {'requirement': 'Python'}
                }
            ]
        }
        mock_session.get.return_value = mock_response

        api = HeadHunterAPI()
        result: list = api.get_vacancies('Python')

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

        vacancy: dict = result[0]

        self.assertEqual(vacancy['name'], 'Test Vacancy')
        self.assertEqual(vacancy['alternate_url'], 'https://example.com/vacancy/1')
        self.assertEqual(vacancy['salary'], {'from': 1000, 'to': 2000})
        self.assertEqual(vacancy['snippet']['requirement'], 'Python')

    @patch('src.api.requests.Session')
    def test_get_vacancies_error_status(self, mock_session_class: 'MagicMock') -> None:
        """
        Тест обработки ошибки при получении вакансий с ошибочным статусом ответа
        Проверяет выброс исключения ConnectionError
        """
        mock_session = mock_session_class.return_value
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_session.get.return_value = mock_response

        api = HeadHunterAPI()

        with self.assertRaises(ConnectionError):
            api.get_vacancies('Python')

    @patch('src.api.requests.Session')
    def test_get_vacancies_empty_items(self, mock_session_class: 'MagicMock') -> None:
        """
         Тест обработки пустого списка вакансий
         """
        # Мокаем ответ без вакансий
        mock_session = mock_session_class.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': []}

        mock_session.get.return_value = mock_response

        api = HeadHunterAPI()

        result: list = api.get_vacancies('Python')

        self.assertEqual(result, [])
