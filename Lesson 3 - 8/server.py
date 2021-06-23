import json
import sys
from socket import socket, AF_INET, SOCK_STREAM

import commands

config = commands.get_configs()


def handle_message(message):
    if config.get('ACTION') in message \
            and message[config.get('ACTION')] == config.get('PRESENCE') \
            and config.get('TIME') in message \
            and config.get('USER') in message \
            and message[config.get('USER')][config.get('ACCOUNT_NAME')] == 'Guest':
        return {config.get('RESPONSE'): 200}
    return {
        config.get('RESPONSE'): 400,
        config.get('ERROR'): 'Bad Request'
    }


def run_server():
    start_range_port = config.get('start_range_port')
    end_range_port = config.get('end_range_port')

    try:
        if '-p' in sys.argv:
            port = int(sys.argv[2])
        else:
            port = config.get('DEFAULT_PORT')
        if not start_range_port <= port <= end_range_port:
            raise ValueError
    except IndexError:
        print(f'После "-p" необходимо указать порт сервера')
        sys.exit(1)
    except ValueError:
        print(f'Порт должен быть указан в диапазоне от {start_range_port} до {end_range_port}')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            address = sys.argv[4]
            print(address)
        else:
            address = ''

    except IndexError:
        print(f'После "-a"- необходимо указать адрес сервера')
        sys.exit(1)

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((address, port))

    server_socket.listen(config.get('MAX_CONNECTIONS'))

    print(f'The server_socket runs on address: {address or "opened"} and port: {port}')
    while True:
        client, client_address = server_socket.accept()
        try:
            message = commands.get_message(client, config)
            response = handle_message(message)
            commands.send_message(client, response, config)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента')
            client.close()


if __name__ == '__main__':
    run_server()
