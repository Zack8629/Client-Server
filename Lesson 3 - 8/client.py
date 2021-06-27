import json
import time
from socket import socket, AF_INET, SOCK_STREAM

import commands

config = commands.get_configs(is_server=False)


def create_presence_message(account_name):
    message = {
        config.get('ACTION'): config.get('PRESENCE'),
        config.get('TIME'): time.time(),
        config.get('USER'): {
            config.get('ACCOUNT_NAME'): account_name
        }
    }
    return message


def handle_response(message):
    if config.get('RESPONSE') in message:
        if message[config.get('RESPONSE')] == 200:
            return '200 : OK'
        return f'400 : {message[config.get("ERROR")]}'
    raise ValueError


def run_client():
    server_address = commands.validate_address() or commands.get_configs().get("DEFAULT_IP_ADDRESS")
    server_port = commands.validate_port()

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((server_address, server_port))
    presence_message = create_presence_message('Guest')
    commands.send_message(server_socket, presence_message, config)
    try:
        response = commands.get_message(server_socket, config)
        handled_response = handle_response(response)
        print(f'Ответ от сервера: {response}')
        print(handled_response)
    except (ValueError, json.JSONDecodeError):
        print('Ошибка декодирования сообщения')


if __name__ == '__main__':
    run_client()
