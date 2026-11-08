import primitive_db.constant as constant
import primitive_db.utils as utils
import primitive_db.parser as parser


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

def insert(metadata, table_name, values):
    if metadata.get(table_name, False):
        columns, err = parser.pars_row(metadata, table_name, values)
    else:
        raise ValueError(f"Таблицы {table_name}, не существует.")
    if err != None:
        if isinstance(err, str):
            err = [err]
        raise ValueError(" ".join(err))
    table_data = utils.load_table_data(table_name)
    table_data = utils.update_id(table_data)
    columns = {"ID":utils.id_gen_next(table_data), **columns}
    finall_table = [*table_data, columns]
    return finall_table

def select(table_data, where_clause=None):
    if where_clause == None:
        return table_data
    else:
        column_where, value_where = parser.parser_where_set(where_clause)

        if set([column_where]).issubset(
            utils.set_unique_keys(table_data)):
            typed_value_where, err = parser.parse_col(
                value_where, 
                type(table_data[0][column_where]).__name__)

            if typed_value_where == None:
                raise ValueError(f"Ошибка выбора столбцов. {" и ".join([err])}")
            
            return [data for data in table_data if data.get(column_where) == typed_value_where]
        raise ValueError(f"Ошибка выбора столбцов. {" и ".join([column_where])}")

def update(table_data, set_clause, where_clause):
    column_set, value_set = parser.parser_where_set(set_clause)
    if column_set == "ID":
        raise ValueError(f"Ошибка, ID в таблице изменить нельзя.")
    column_where, value_where = parser.parser_where_set(where_clause)
    set_where_keys = {column_set, column_where}
    
    
    if set_where_keys.issubset(utils.set_unique_keys(table_data)):
        typed_value_where, err = parser.parse_col(
                    value_where, 
                    type(table_data[0][column_where]).__name__) 
        typed_value_set = parser.parse_col(
                    value_set, 
                    type(table_data[0][column_where]).__name__)
        
        if typed_value_where == None or typed_value_set == None:
            raise ValueError(f"Ошибка выбора столбцов. {" и ".join([err])}")
        id_values = [data["ID"]
                    for data in table_data
                    if data.get(column_where) == typed_value_where]
        update_table = [
            {**data, column_set:typed_value_set} 
            if data.get(column_where) == typed_value_where 
            else data 
            for data in table_data
        ]
        return update_table, id_values
    else:
        raise ValueError(f"Ошибка выбора столбцов.")

def delete(table_data, where_clause):
    column_where, value_where = parser.parser_where_set(where_clause)
    
    if set([column_where]).issubset(
                utils.set_unique_keys(table_data)):
        typed_value_where, err = parser.parse_col(
                    value_where, 
                    type(table_data[0][column_where]).__name__)
        if typed_value_where == None:
            raise ValueError(f"Ошибка выбора столбцов. {" и ".join([err])}")

        id_values = [data["ID"]
                            for data in table_data
                            if data.get(column_where) == typed_value_where]
        
        update_table = [
            {**data} for data in table_data 
            if data.get(column_where) != typed_value_where
        ]
        return update_table, id_values
    raise ValueError(f"Ошибка выбора столбцов. {" и ".join([column_where])}")
