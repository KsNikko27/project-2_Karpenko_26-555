

def parser_where_set(column):
    """Разбирает пару «столбец = значение»:
        проверяет разделитель и возвращает кортеж
        (столбец, значение)."""
    colum_clause, equal, value_clause = column
    if equal != "=":
        raise ValueError(f"Ошибка. Ожидалось: \"=\". Введенное значение: {equal}")
    
    return colum_clause, value_clause   

def parse_values(raw):
    """Разбирает строку вида (значение1, ...)
    и возвращает кортеж очищенных значений."""
    raw = raw.strip()
    if not (raw[0].startswith("(") and raw[-1].endswith(")")):
        raise ValueError('Ожидались значения в скобках: values (<значения>)')
    inner = raw[1:-1]
    inner = [v.strip().strip(",\"'") for v in inner.split(",")]
    return tuple(inner)

def pars_row(metadata, table_name, valuses):
    """Парсит значения строки по данным таблицы:
        сверяет количество столбцов и типы;
        возвращает (словарь значений, None)
        или (None, список ошибок)."""
    columns = metadata[table_name]
    erros = []
    parsed = {}
    input_columns = [c for c in columns if c != "ID"]
    if len(input_columns) != len(valuses):
        return None, f"Ожидалось {len(input_columns)} значений"
    for col, row in zip(input_columns, valuses):
        expect_type = columns[col]
        value, err = parse_col(row, expect_type)
        if err:
            erros.append(f"колонка {col} : {err}")
        else:
            parsed[col] = value
    if erros:
        return None, erros
    return parsed, None


def parse_col(col, expect_type):
    """Приводит значение к ожидаемому типу (int, str, bool);
        возвращает (значение, None) при успехе
        или (None, сообщение об ошибке)."""
    if expect_type == "int":
        try:
            return int(col), None
        except ValueError:
            return None, f"ожидалось целое число (int), получено: {col}"
    if expect_type == "str":
        if isinstance(col, str):
            return col, None    
        else:
            return None, f"Ожидалась строка '<значение>' , получено {col}"
            
    if expect_type == "bool":
        if col.lower() in ["true", 1, "1"]:
            return True, None
        elif col.lower() in ["false", 0, "0"]:
            return False, None
        else:
            return None, f"ожидалось true/false, получено: {col}"
    return None, f"неизвестный тип колонки: '{expect_type}'"
