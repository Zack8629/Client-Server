from subprocess import Popen, CREATE_NEW_CONSOLE


def run_multiple_clients(num_client: int, file: str):
    list_processes = []  # Список клиентских процессов
    num_client = num_client  # Количество открытий клиентов
    file = file  # Файл для запуска клиентов

    while True:
        user_command = input(f'Запустить {num_client} клиентов-(s) / Закрыть клиентов-(x) / Выйти-(q) -> ')

        if user_command == 'q':
            print('Завершение скрипта!')
            break
        elif user_command == 's':
            for _ in range(num_client):
                # Флаг CREATE_NEW_CONSOLE нужен для ОС Windows,
                # чтобы каждый процесс запускался в отдельном окне консоли
                list_processes.append(Popen(f'python {file}',
                                            creationflags=CREATE_NEW_CONSOLE))
            print(f'Запущено {num_client} клиентов')
        elif user_command == 'x':
            for p in list_processes:
                p.kill()
            list_processes.clear()
            print('Клиенты закрыты')


if __name__ == '__main__':
    client_num = 2
    run_file = 'client_r.py'

    run_multiple_clients(client_num, run_file)
