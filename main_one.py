from src.api import HeadHunterAPI
from src.storage import JSONVacancyStorage
from src.models import Vacancy
from src.utils import filter_vacancies, get_top_n_vacancies, get_vacancies_by_salary, print_vacancies


def user_interaction():
    api_platforms = {
        "hh.ru": HeadHunterAPI()
    }

    print("Доступные платформы:")
    for platform in api_platforms.keys():
        print(f"- {platform}")

    platform_choice = input("Выберите платформу (введите название): ").strip()

    api_instance = api_platforms.get(platform_choice.lower())

    if not api_instance:
        print("Платформа не найдена.")
        return

    search_query = input("Введите поисковый запрос (например 'Python'): ").strip()

    print("Получение вакансий...")
    raw_data = api_instance.get_vacancies(search_query)

    vacancies_list = Vacancy.cast_to_object_list(raw_data)

    storage_choice = input("Вы хотите сохранить вакансии в файл? (да/нет): ").strip().lower()

    storage_handler = JSONVacancyStorage()

    for vac in vacancies_list:
        storage_handler.add_vacancy(vac)

    while True:
        print("\nДоступные операции:")
        print("1 - Вывести топ N вакансий по зарплате")
        print("2 - Фильтровать вакансии по ключевым словам")
        print("3 - Получить вакансии по диапазону зарплат")
        print("4 - Показать все сохранённые вакансии")
        print("5 - Удалить вакансию по ссылке")
        print("6 - Выйти")

        choice = input("Выберите операцию (номер): ").strip()

        if choice == '1':
            n_str = input("Введите N (количество вакансий): ")
            try:
                n = int(n_str)
            except ValueError:
                print("Некорректное число.")
                continue
            all_vacs = storage_handler.get_all_vacancies()
            top_n = get_top_n_vacancies(all_vacs, n)
            print(f"\nТоп {n} вакансий по зарплате:")
            print_vacancies(top_n)

        elif choice == '2':
            keywords_input = input("Введите ключевые слова через пробел: ")
            keywords = keywords_input.strip().split()
            all_vacs = storage_handler.get_all_vacancies()
            filtered = filter_vacancies(all_vacs, keywords)
            print(f"\nВакансии по ключевым словам '{keywords_input}':")
            print_vacancies(filtered)

        elif choice == '3':
            min_sal_input = input("Введите минимальную зарплату (или оставьте пустым): ")
            max_sal_input = input("Введите максимальную зарплату (или оставьте пустым): ")
            min_sal = int(min_sal_input) if min_sal_input.strip().isdigit() else None
            max_sal = int(max_sal_input) if max_sal_input.strip().isdigit() else None

            all_vacs = storage_handler.get_all_vacancies()
            ranged = get_vacancies_by_salary(all_vacs, min_salary=min_sal, max_salary=max_sal)
            print("Вакансии в диапазоне зарплат:")
            print_vacancies(ranged)

        elif choice == '4':
            all_vacs = storage_handler.get_all_vacancies()
            print("\nВсе сохранённые вакансии:")
            print_vacancies(all_vacs)

        elif choice == '5':
            link_to_delete = input("Введите ссылку на вакансию для удаления: ").strip()

        elif choice == '6':
            print("Хорошего дня! До свидания!")
            break


if __name__ == "__main__":
    user_interaction()
