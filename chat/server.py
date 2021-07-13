import json
import logging
from select import select
from socket import socket, AF_INET, SOCK_STREAM

from services import commands
from services.logs_decorator import log
from settings import server_log_config

server_name_logger = server_log_config.name_logger
server_logger = logging.getLogger(server_name_logger)

config = commands.get_configs(server_name_logger)


@log
def handle_message(message):
    if config.get('ACTION') in message \
            and message[config.get('ACTION')] == config.get('PRESENCE') \
            and config.get('TIME') in message \
            and config.get('USER') in message \
            and message[config.get('USER')][config.get('ACCOUNT_NAME')] == 'Guest':
        server_logger.debug(f'Ответ успешно сформирован - КОД = 200')
        return {config.get('RESPONSE'): 200}

    server_logger.error(f'Некорректное сообщение от клиента "{message}". Ответ от сервера - КОД = 400')
    return {
        config.get('RESPONSE'): 400,
        config.get('ERROR'): 'Bad Request'
    }


@log
def run_server():
    address = commands.validate_address(server_name_logger)
    port = commands.validate_port(server_name_logger)

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(config.get('MAX_CONNECTIONS'))
    server_socket.settimeout(config.get('TIMEOUT'))

    server_logger.info(f'The server runs at:{address or config.get("DEFAULT_IP_ADDRESS")} port: {port}')
    print(f'The server runs at:{address or config.get("DEFAULT_IP_ADDRESS")} port: {port}')

    list_connected_clients = []
    while True:
        try:
            client, client_address = server_socket.accept()

        except OSError:
            pass
        else:
            list_connected_clients.append(client)
            print(f'Установлено соедение с {client_address}')
            server_logger.info(f'Установлено соедение с {client_address}')

        read_clients, write_clients, err_list = [], [], []
        try:
            read_clients, write_clients, err_list = select(list_connected_clients,
                                                           list_connected_clients,
                                                           [], 0)
        except OSError:
            pass

        commands.get_requests_clients(read_clients,
                                      write_clients,
                                      list_connected_clients,
                                      config,
                                      server_name_logger)


if __name__ == '__main__':
    run_server()
