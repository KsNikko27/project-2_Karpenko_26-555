import json

import primitive_db.constant as constant


def load_metadata(filepath):
    """Загружает данные таблиц базы из JSON-файла;
        при отсутствии файла или ошибке чтения
        возвращает пустой список."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return dict()
    except json.JSONDecodeError:
        return dict()

def save_metadata(filepath, data):
    """Сохраняет данные таблиц базы в JSON-файл с отступами."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file,ensure_ascii=False, indent=4)
    

def load_table_data(table_name):
    """Загружает данные таблицы из JSON-файла по имени;
        при отсутствии файла или ошибке чтения возвращает пустой список."""
    filepath = constant.DIR_DATA[0] + table_name + constant.DIR_DATA[1]
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            columns = json.load(file)
            return columns
    except FileNotFoundError:
            #print(f"Такой табл {filepath} не существует")
            return []
    except json.JSONDecodeError:
            return []

def save_table_data(table_name, columns):
    """Сохраняет данные строк таблицы в JSON-файл."""
    filepath = constant.DIR_DATA[0] + table_name + constant.DIR_DATA[1]
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(columns, file,ensure_ascii=False, indent=4)

def split_command(command):
    """Разбирает команду create table:
        проверяет имя (не с цифры)
        и столбцы формата «имя:тип»;
        возвращает (имя, словарь столбцов)."""
    if command[0] == constant.CREATE_TABLE_COMMAND[0]:
        if len(command) < 3:
            raise ValueError(f"Некорректное значение: {" ".join(command)
                                                   }. Попробуйте снова.")
        if command[1][0].isdigit():
            raise ValueError("Ошибка. Имя таблицы должно начинаться с буквы.")
        columns = {}
        for col in command[2:]:
            name, sep, dtype = col.strip().partition(":")
            if sep != ":" or not name or not dtype:
                raise ValueError(f"Некорректное значение: {"".join([name,sep,dtype])
                                                       }. Попробуйте снова.")
            columns[name] = dtype
        return command[1], columns
    elif command[:2] == constant.CREATE_TABLE_COMMAND[2:4]:
        pass

def id_gen_next(columns):
    """Возвращает следующий ID для таблицы:
        максимум по существующим ID + 1,
        для пустой таблицы 1."""
    if columns:
        value_id = [value["ID"] for value in columns]
        id_gen = max(value_id) + 1
        return id_gen
    else:
        return 1
def set_unique_keys(table_data):
    """Возвращает множество всех имён столбцов,
        встречающихся в строках таблицы."""
    unque_keys = {key for data in table_data for key in data.keys()}
    return unque_keys


def update_id(table_data):
        """Перенумеровывает ID строк по порядку (1, 2, 3...);
            если у строки нет ID то бросает ValueError."""
        for i, data in enumerate(table_data, start=1):
            if data.get("ID", False):
                data["ID"] = i
            else:
                raise ValueError(f"Неизвестная ошибка {update_id.__name__}")
            
        return table_data

