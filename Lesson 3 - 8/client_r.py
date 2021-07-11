from socket import socket, AF_INET, SOCK_STREAM

from services import commands
from settings import client_log_config

client_name_logger = client_log_config.name_logger

config = commands.get_configs(client_name_logger, is_server=False)


def run_client_r():
    server_address = commands.validate_address(client_name_logger) or \
                     commands.get_configs(client_name_logger).get("DEFAULT_IP_ADDRESS")
    server_port = commands.validate_port(client_name_logger)

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((server_address, server_port))

    print(f'Client_R connected!')
    while True:
        response = server_socket.recv(config.get('MAX_PACKAGE_LENGTH'))
        if response:
            data = response.decode('utf-8')
            print(f'Message: {data}')


if __name__ == '__main__':
    run_client_r()
