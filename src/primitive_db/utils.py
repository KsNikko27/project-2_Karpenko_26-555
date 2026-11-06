import json


def load_metadata(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        #print(f"Файла {filepath} не существует")
        return {}
    except json.JSONDecodeError:
        return {}

def save_metadata(filepath, data):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file,ensure_ascii=False, indent=4)
    
def split_command(command):
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
