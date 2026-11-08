import json

import primitive_db.constant as constant


def load_metadata(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        #print(f"Файла {filepath} не существует")
        return list()
    except json.JSONDecodeError:
        return list()

def save_metadata(filepath, data):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file,ensure_ascii=False, indent=4)
    

def load_table_data(table_name):
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
    filepath = constant.DIR_DATA[0] + table_name + constant.DIR_DATA[1]
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(columns, file,ensure_ascii=False, indent=4)

def split_command(command):
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
    if columns:
        value_id = [value["ID"] for value in columns]
        id_gen = max(value_id) + 1
        return id_gen
    else:
        return 1
def set_unique_keys(table_data):
    unque_keys = {key for data in table_data for key in data.keys()}
    return unque_keys


def update_id(table_data):
        for i, data in enumerate(table_data, start=1):
            if data.get("ID", False):
                data["ID"] = i
            else:
                raise ValueError(f"Неизвестная ошибка {update_id.__name__}")
            
        return table_data

