import json
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
    address = commands.validate_address()
    port = commands.validate_port()

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(config.get('MAX_CONNECTIONS'))

    print(f'The server runs at:{address or config.get("DEFAULT_IP_ADDRESS")} port: {port}')
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
