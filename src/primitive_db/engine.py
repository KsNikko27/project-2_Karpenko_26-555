import shlex

import prompt
from prettytable import PrettyTable

import primitive_db.constant as constant
import primitive_db.core as core
import primitive_db.utils as utils
import primitive_db.parser as parser


def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\n***Операции с данными***")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) " +
          "- создать запись.")
    print("<command> select from <имя_таблицы> where <столбец> = <значение>" +
          " - прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1>",
          "where <столбец_условия> = <значение_условия> - обновить запись.")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 


def run():
    print_help()
    metadata = utils.load_metadata(constant.DIR_JSON)
    for table in metadata:
        table_data = utils.load_table_data(table)
        utils.save_table_data(table, table_data)
    while True:
        user_input = prompt.string("Введите команду: ")
        try:
            args = shlex.split(user_input)
        except ValueError:
            print(f"Некорректное значение: {user_input}. Попробуйте снова.")
            continue
##############################EXIT#########################
        if constant.EXIT_COMMAND == args:
            break
##############################HELP#########################
        elif constant.HELP_COMMAND == args:
            print_help()
##############################LIST_TABLES#########################
        elif constant.LIST_TABLE_COMMAND == args:
            metadata = utils.load_metadata(constant.DIR_JSON)
            core.list_tables(metadata)
##############################CREATE_TABLE#########################            
        elif args[0] == constant.CREATE_TABLE_COMMAND[0]:
            metadata = utils.load_metadata(constant.DIR_JSON)
            try:
                table_name, columns = utils.split_command(args)
            except IndexError:
                print(f"Некорректное значение: {" ".join(args)}. Попробуйте снова.")
                continue
            except TypeError:
                print(f"Некорректное значение: {" ".join(args)}. Попробуйте снова.")
                continue
            except ValueError as e:
                print(e)
                continue
            try:
                core.create_table(metadata, table_name, columns)
                utils.save_metadata(constant.DIR_JSON, metadata)
                col_str = ", ".join(f"{n}:{t}" for n, t in metadata[table_name].items())
                print(f"Таблица \"{table_name
                                   }\" успешно создана со столбцами: {col_str}"
                                   )
            except ValueError as e:
                print(e)
#############################DROP_TABLE##########################                
        elif args[0] == constant.CREATE_TABLE_COMMAND[1]:
            metadata = utils.load_metadata(constant.DIR_JSON)
            try:
                core.drop_table(metadata, args[1])
                utils.save_table_data(args[1], [])
                utils.save_metadata(constant.DIR_JSON, metadata)

            except IndexError:
                print(f"Некорректное значение: {" ".join(args)}. Попробуйте снова.")
                continue
            except ValueError as e:
                print(e)
                continue
##########################INSERT#############################
        elif args[0]== constant.INSERT:
            #insert into users values ("Sergei", 28, true)
            try:
                table_data = handle_insert(args[1:])
            except ValueError as e:
                print(e)
                continue
            try:
                utils.save_table_data(args[2], table_data)
            except ValueError as e:
                print(e)
                continue
            print(f"Запись с ID={
                table_data[-1]["ID"]} успешно добавлена в таблицу \"{
                args[2]}\".")
##########################SELECT#############################
        elif args[0] == constant.SELECT:
            try:
                table_data = handle_select(args[1:])
                table_keys = table_data[0].keys()
            except ValueError as e:
                print(e)
                continue

            table = PrettyTable()
            table.field_names = table_keys
            value_data = [[key[col] for col in key] for key in table_data]
            table.add_rows(value_data)
            print(table)
##########################UPDATE#############################
        elif args[0] == constant.UPDATE:
            #update users set age = 29 where name = "Sergei"
            try:
                table_data, id_list= handle_update(args[1:])
                """if table_data == []:
                    print(f"Таблица {args[2]} пуста.")
                    continue"""
            except ValueError as e:
                print(e)
                continue
            utils.save_table_data(args[1], table_data)
            if id_list == []:
                print("Изменений не зафиксированно")
                continue
            print(f"Запись с ID={
                ", ".join([str(ids) for ids in id_list])} успешно добавлена в таблицу \"{
                args[1]}\".")           
##########################DELETE#############################
        elif args[0] == constant.DELETE:
            #delete from <имя_таблицы> where <столбец> = <значение>
            try:
                table_data, id_list = handle_delete(args[1:])
            except ValueError as e:
                print(e)
                continue
            try:
                table_data = utils.update_id(table_data)  
                utils.save_table_data(args[2], table_data)
                if id_list == []:
                    print("Изменений не зафиксированно")
                    continue
                print(f"Запись с ID={
                        ", ".join([str(ids) for ids in id_list])} удалена из таблицы \"{
                        args[2]}\".")
                print(f"ID таблицы \"{args[2]}\" обновлены.")

            except ValueError as e:
                print(e)         
                continue
##########################info#############################
        elif args[0] == constant.INFO:
            if len(args) != 2:
                print(f"Некорректное значение: {" ".join(args)}. Попробуйте снова.")
                continue
            metadata = utils.load_metadata(constant.DIR_JSON)   
            table_name = args[1]   
            if table_name not in metadata:
                print(f"Таблицы '{table_name}' нет.")
                continue
            table_data = utils.load_table_data(table_name)
            print(f"Таблица: {table_name}")
            print(f"Столбцы: " +
                  ", ".join([f"{key}:{metadata[table_name][key]}" for key in metadata[table_name]]) )
            print(f"Количество записей: {len(table_data)}")
            continue
                   
        else:
            print(f"Функции \"{" ".join(args)}\" нет. Попробуйте снова.")

 


def handle_insert(args):
    if len(args) < 3 or args[0] != constant.INTO:
        raise ValueError("Формат: insert into <таблица> values (<значение1>, ...)")
    table_name = args[1]
    metadata = utils.load_metadata(constant.DIR_JSON)
    if table_name not in metadata:
        raise ValueError(f'Таблицы "{table_name}" не существует.')
    if args[2] != constant.VALUES:
        raise ValueError("Формат: insert into <таблица> values (<значение1>, ...)")
    if args[3:]:
        try:
            tup_args = parser.parse_values(" ".join(args[3:]))
        except ValueError as e:
            raise e
        try:
            table_data = core.insert(metadata, table_name, tup_args)
        except ValueError as e:
            raise e
        return table_data
    raise ValueError("Формат: insert into <таблица> values (<значение1>, ...)")

def handle_select(args):
    #from users where age = 28
    if len(args) < 2 or args[0] != constant.FROM:
        raise ValueError(
                "Формат: select from <имя_таблицы> where <столбец> = <значение>. " + 
                "\nИли select from <имя_таблицы>")
    
    table_name = args[1]
    metadata = utils.load_metadata(constant.DIR_JSON)
    if table_name not in metadata:
        raise ValueError(f'Таблицы "{table_name}" не существует.')
        
    table_data = utils.load_table_data(table_name)
    if table_data == []:
        raise ValueError(f"Таблица {table_name} пуста")
    if len(args) == 2:
        table_data = core.select(table_data)
        return table_data
    
    if args[2] == constant.WHERE:
        if len(args[3:]) == 3:
            table_data = core.select(table_data, tuple(args[3:]))
            return table_data
        elif args[3:]:
            column, sep, value = "".join(args[3:]).partition("=")
            if "" in (column, sep, value):
                raise ValueError(f"Ошибка: ожидается <столбец> = <значение>, " +
                                f"получено: \"{column}{sep}{value}\"")
            table_data = core.select(table_data, (column,sep,value))
            return table_data
                            
        else:
            raise ValueError(f"Ошибка: ожидается <столбец> = <значение>, " +
                                     f"получено \"{"".join(args[3:])}\"")
    else:
        raise ValueError(f"Ошибка: ожидается <столбец> = <значение>, " +
                                         f"получено \"{"".join(args[3:])}\"")

def handle_update(args):
    
    #users set age = 29 where name = "Sergei"
    if len(args) < 4 or args[1] != constant.SET:
        raise ValueError(
            "Формат: update <имя_таблицы> "+
            "set <столбец> = <значение> where <столбец> = <значение>. ")
       
    table_name = args[0]
    metadata = utils.load_metadata(constant.DIR_JSON)
    if table_name not in metadata:
        raise ValueError(f'Таблицы "{table_name}" не существует.')
    table_data = utils.load_table_data(table_name)
    if table_data == []:
        raise ValueError(f"Нечего изменять. Таблица {table_name} пуста")
    #age = 29 where name = "Sergei"
    
    firs_args, where, sec_args = " ".join(args[2:]).partition(constant.WHERE)
    if "" in (firs_args, where, sec_args):
        raise ValueError((f"Ошибка: " +
                "ожидается set <столбец> = <значение>, " +
                "where <столбец> = <значение> " +
                f"получено \"{" ".join(args[2:])}\""))
    #age = 29 | name = "Sergei"
    col_set, sep_set, val_set =  firs_args.partition('=')
    col_where, sep_where, val_where =  sec_args.partition('=')
    if "" in (col_set, sep_set, val_set,
                     col_where, sep_where, val_where):
        raise ValueError((f"Ошибка: " +
                "ожидается set <столбец> = <значение>, " +
                "where <столбец> = <значение> " +
                f"получено \"{" ".join(args[2:])}\""))
    
    
    table_data, id_list = core.update(table_data, (col_set.strip(), sep_set, val_set.strip()),
                (col_where.strip(), sep_where, val_where.strip()))
    return table_data, id_list

def handle_delete(args):   
    #from <имя_таблицы> where <столбец> = <значение>
    if len(args) < 3 or args[0] != constant.FROM:
        raise ValueError(
                    "Формат: delete from <имя_таблицы> "+
                    "where <столбец> = <значение>.")
    table_name = args[1]
    metadata = utils.load_metadata(constant.DIR_JSON)
    if table_name not in metadata:
        raise ValueError(f'Таблицы "{table_name}" не существует.')
    table_data = utils.load_table_data(table_name)
    if table_data == []:
        raise ValueError(f"Нечего удалять. Таблица {table_name} пуста")
    if args[2] != constant.WHERE and args[3:] == []:
        raise ValueError("Ошибка условия where <столбец> = <значение> " +
                         f'получено \"{" ".join(args[2:])}".')

    col_where, sep_where, val_where =  " ".join(args[3:]).partition('=')
    if "" in (col_where, sep_where, val_where):
        raise ValueError("Ошибка аргументов <столбец> = <значение> " +
                            f'получено \"{" ".join(args[3:])}".')
    table_data, id_list = core.delete(table_data, 
                                      (col_where.strip(), sep_where, val_where.strip()))
    return table_data, id_list 


run()


