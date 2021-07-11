import json
import logging
import time
from socket import socket, AF_INET, SOCK_STREAM

from services import commands
from services.logs_decorator import log
from settings import client_log_config

client_name_logger = client_log_config.name_logger
client_logger = logging.getLogger(client_name_logger)

config = commands.get_configs(client_name_logger, is_server=False)


@log
def create_presence_message(account_name):
    message = {
        config.get('ACTION'): config.get('PRESENCE'),
        config.get('TIME'): time.time(),
        config.get('USER'): {
            config.get('ACCOUNT_NAME'): account_name
        }
    }
    return message


@log
def handle_response(message):
    if config.get('RESPONSE') in message:
        if message[config.get('RESPONSE')] == 200:
            return '200 : OK'
        return f'400 : {message[config.get("ERROR")]}'
    raise ValueError


@log
def run_client():
    server_address = commands.validate_address(client_name_logger) or \
                     commands.get_configs(client_name_logger).get("DEFAULT_IP_ADDRESS")
    server_port = commands.validate_port(client_name_logger)

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((server_address, server_port))

    presence_message = create_presence_message('Guest')
    commands.send_message(server_socket, presence_message, config)
    try:
        response = commands.get_message(server_socket, config)
        handled_response = handle_response(response)

        # print(f'Ответ от сервера: {response}')
        # print(handled_response)

        client_logger.debug(f'Ответ от сервера: {response}')
        client_logger.debug(handled_response)

    except (ValueError, json.JSONDecodeError):
        client_logger.error('Ошибка декодирования сообщения')
        # print('Ошибка декодирования сообщения')

    client_logger.info(
        f'Client connected at address: {server_address or config.get("DEFAULT_IP_ADDRESS")} port: {server_port}'
    )


if __name__ == '__main__':
    run_client()
