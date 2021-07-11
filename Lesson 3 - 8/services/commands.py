import json
import logging
import sys

from settings import client_log_config, server_log_config
from settings.configs import default_parameters

client_name_logger = client_log_config.name_logger
client_logger = logging.getLogger(client_name_logger)

server_name_logger = server_log_config.name_logger
server_logger = logging.getLogger(server_name_logger)


def get_logger(name_logger):
    if name_logger == 'client':
        return client_logger
    else:
        return server_logger


def get_configs(name_logger: str, is_server=True):
    config_keys = [
        'DEFAULT_PORT',
        'MAX_CONNECTIONS',
        'MAX_PACKAGE_LENGTH',
        'ENCODING',
        'ACTION',
        'TIME',
        'USER',
        'ACCOUNT_NAME',
        'PRESENCE',
        'RESPONSE',
        'ERROR',
        'START_RANGE_PORT',
        'END_RANGE_PORT',
        'TIMEOUT',
    ]

    if not is_server:
        config_keys.append('DEFAULT_IP_ADDRESS')

    for key in config_keys:
        if key not in default_parameters:
            error_text = f'В файле конфигураций не хватает ключа: {key}'
            get_logger(name_logger).error(error_text)
            print(error_text)

            sys.exit(1)
    return default_parameters


def send_message(opened_socket, message, configs):
    json_message = json.dumps(message)
    response = json_message.encode(configs.get('ENCODING'))
    opened_socket.send(response)


def get_message(opened_socket, configs):
    response = opened_socket.recv(configs.get('MAX_PACKAGE_LENGTH'))
    if isinstance(response, bytes):
        json_response = response.decode(configs.get('ENCODING'))
        response_dict = json.loads(json_response)
        if isinstance(response_dict, dict):
            return response_dict
        raise ValueError
    raise ValueError


def validate_address(name_logger):
    try:
        if '-a' in sys.argv:
            address = sys.argv[2]
        else:
            address = ''

    except IndexError:
        error_text = f'После "-a" необходимо указать адрес сервера'
        get_logger(name_logger).error(error_text)
        print(error_text)

        sys.exit(1)
    return address


def validate_port(name_logger):
    argument_number = 2
    if validate_address(name_logger):
        argument_number = 4

    config = get_configs(name_logger)
    start_range_port = config.get('START_RANGE_PORT')
    end_range_port = config.get('END_RANGE_PORT')

    try:
        if '-p' in sys.argv:
            port = int(sys.argv[argument_number])
        else:
            port = config.get('DEFAULT_PORT')

        if not start_range_port <= port <= end_range_port:
            raise ValueError
    except IndexError:
        error_text = f'После "-p" необходимо указать порт сервера'
        get_logger(name_logger).error(error_text)
        print(error_text)

        sys.exit(1)
    except ValueError:
        error_text = f'Порт должен быть указан в диапазоне от {start_range_port} до {end_range_port}'
        get_logger(name_logger).error(error_text)
        print(error_text)

        sys.exit(1)
    return port


def get_requests_clients(read_clients, write_clients, list_connected_clients, configs, name_logger):
    for r_sock in read_clients:
        try:
            message = r_sock.recv(configs.get('MAX_PACKAGE_LENGTH'))
            for sock in write_clients:
                try:
                    sock.send(message)
                except Exception as e:
                    error_text = f'COMMANDS remove {sock} err == {e}'
                    get_logger(name_logger).error(error_text)
                    print(f'COMMANDS remove {sock} err == {e}')
                    list_connected_clients.remove(sock)
        except Exception as e:
            error_text = f'DONE ERR {e}'
            get_logger(name_logger).error(error_text)
            print('*' * 10)
            print(f'COMMANDS DONE ERR {e}')
