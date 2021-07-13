from subprocess import Popen, CREATE_NEW_CONSOLE


def run_multiple_clients(file: str, num_client: int = 5):
    list_processes = []  # Список клиентских процессов
    num_client = num_client  # Количество открытий клиентов
    file = file  # Файл для запуска клиентов

    while True:
        user_command = input(f'Запустить {num_client} экземпляра(ов) "{file}"-(s) / Закрыть клиентов-(x) / Выйти-(q) -> ')

        if user_command == 'q':
            print('Завершение скрипта!')
            break
        elif user_command == 's':
            for _ in range(num_client):
                # Флаг CREATE_NEW_CONSOLE нужен для ОС Windows,
                # чтобы каждый процесс запускался в отдельном окне консоли
                list_processes.append(Popen(f'python {file}',
                                            creationflags=CREATE_NEW_CONSOLE))
            print(f'Запущено {num_client} экземпляра(ов) "{file}')
        elif user_command == 'x':
            for p in list_processes:
                p.kill()
            list_processes.clear()
            print('"кземпляры закрыты')
        else:
            print('Неверная команда! Попробуйте ещё раз.')


if __name__ == '__main__':
    run_file = 'client_1.py'
    client_num = 3

    run_multiple_clients(run_file, client_num)
