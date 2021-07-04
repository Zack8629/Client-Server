import json
import logging
from socket import socket, AF_INET, SOCK_STREAM

import commands
from settings import server_log_config

server_name_logger = server_log_config.name_logger
server_logger = logging.getLogger(server_name_logger)

config = commands.get_configs(server_name_logger)


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
    address = commands.validate_address(server_name_logger)
    port = commands.validate_port(server_name_logger)

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(config.get('MAX_CONNECTIONS'))

    server_logger.info(f'The server runs at:{address or config.get("DEFAULT_IP_ADDRESS")} port: {port}')
    print(f'The server runs at:{address or config.get("DEFAULT_IP_ADDRESS")} port: {port}')
    while True:
        client, client_address = server_socket.accept()
        try:
            message = commands.get_message(client, config)
            response = handle_message(message)
            commands.send_message(client, response, config)
            client.close()
        except (ValueError, json.JSONDecodeError):
            server_logger.error('Принято некорретное сообщение от клиента')
            # print('Принято некорретное сообщение от клиента')
            client.close()


if __name__ == '__main__':
    run_server()
