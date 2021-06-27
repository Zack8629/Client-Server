import json
import sys

from configs import default_parameters


def get_configs(is_server=True):
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
    ]

    if not is_server:
        config_keys.append('DEFAULT_IP_ADDRESS')

    for key in config_keys:
        if key not in default_parameters:
            print(f'В файле конфигураций не хватает ключа: {key}')
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


def validate_address():
    try:
        if '-a' in sys.argv:
            address = sys.argv[2]
        else:
            address = ''

    except IndexError:
        print(f'После "-a"- необходимо указать адрес сервера')
        sys.exit(1)

    return address


def validate_port():
    argument_number = 2
    if validate_address():
        argument_number = 4

    config = get_configs()
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
        print(f'После "-p" необходимо указать порт сервера')
        sys.exit(1)
    except ValueError:
        print(f'Порт должен быть указан в диапазоне от {start_range_port} до {end_range_port}')
        sys.exit(1)

    return port
