import shlex

import prompt

import primitive_db.constant as constant
import primitive_db.core as core
import primitive_db.utils as utils


def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 


def run():
    print_help()
    while True:
        user_input = prompt.string("Введите команду: ")
        try:
            args = shlex.split(user_input)
        except ValueError:
            print(f"Некорректное значение: {user_input}. Попробуйте снова.")
            continue
        if constant.EXIT_COMMAND == args:
            break
        elif constant.HELP_COMMAND == args:
            print_help()
        elif constant.LIST_TABLE_COMMAND == args:
            metadata = utils.load_metadata(constant.DIR_JSON)
            core.list_tables(metadata)
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
                col_str = ", ".join(f"{n}:{t}" for n, t in columns.items())
                print(f"Таблица \"{table_name
                                   }\" успешно создана со столбцами: {col_str}"
                                   )
            except ValueError as e:
                print(e)
        elif args[0] == constant.CREATE_TABLE_COMMAND[1]:
            metadata = utils.load_metadata(constant.DIR_JSON)
            try:
                core.drop_table(metadata, args[1])
                utils.save_metadata(constant.DIR_JSON, metadata)
            except IndexError:
                print(f"Некорректное значение: {" ".join(args)}. Попробуйте снова.")
                continue
            except ValueError as e:
                print(e)
                continue
        else:
            print(f"Функции {" ".join(args)} нет. Попробуйте снова.")

