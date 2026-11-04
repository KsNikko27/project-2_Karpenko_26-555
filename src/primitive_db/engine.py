import prompt


def welcome():
    print("Первая попытка запустить проект!")
    print("\n***")
    print("<comand> exit - выйти из программы")
    print("<command> help - справочная информация")
    while True:
        read_comand = prompt.string("Введите команду: ")
        if read_comand == "exit":
            break
        elif read_comand == "help":

            print("\n<comand> exit - выйти из программы")
            print("<command> help - справочная информация")