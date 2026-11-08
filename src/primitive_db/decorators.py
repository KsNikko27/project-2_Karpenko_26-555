import time

import prompt


def handle_db_errors(func):
    """Декоратор для обработки ошибок при работе с базой данных.
        Параметры:
        func (callable): декорируемая функция, выполняющая операции с БД.

        Возвращает:
        callable: обёрнутая функция с встроенной обработкой ошибок.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден" +
                  "Возможно, база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper


def confirm_action(action_name):
    """Декоратор, запрашивающий подтверждение действия 
        у пользователя перед выполнением."""
    def wrapper(*args, **kwargs):
        while True:
            user_input = prompt.string(
                "Вы действительно хотите выполнить удаление? [y/n]:")
            if user_input == "y":
                return action_name(*args, **kwargs)
            else:
                raise ValueError
    return wrapper

def log_time(func):
    """Декоратор для замера и вывода времени
        выполнения функции (в секундах)."""
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)  
        duration = time.monotonic() - start 
        print(f"Функция {func.__name__} выполнилась за {duration:.3f} секунд")
        return result
    return wrapper

def create_cacher():
    """Создаёт функцию кэширования результатов:
    возвращает сохранённое значение по ключу
     или вычисляет его через value_func()."""
#Есть сомнения что данные будут не актуальны после записи
    cache = {}
    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result
    return cache_result