import primitive_db.constant as constant


def create_table(metadata, table_name, columns):
    if columns.get("ID") != "int":
        columns = {"ID":"int", **columns}
    if not all([colum in constant.COLOMN_TYPES for colum in columns.values()]):
        raise ValueError("\nОшибка: Тип должен быть bool, str или int.")
    if table_name not in metadata.keys():
        metadata[table_name] = {**columns}
        return metadata
    else:
        raise ValueError(f"\nОшибка: Таблица \"{table_name}\" уже существует.")

def drop_table(metadata, table_name):
    if table_name not in metadata.keys():
        raise ValueError(f"Ошибка: Таблица \"{table_name}\" не существует.")
    else:
        metadata.pop(table_name)
        print(f"Таблица \"{table_name}\" успешно удалена.")
        return metadata
    
def list_tables(metadata):
    if not metadata:
        print("Таблиц пока нет.")
    else:
        name_table = sorted(metadata.keys())
        for name in name_table:
            print(f"-{name}")
    