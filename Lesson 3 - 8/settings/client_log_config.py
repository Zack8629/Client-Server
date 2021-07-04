import logging

name_logger = 'client'
path = f'logs/{name_logger}.log'

if __name__ == '__main__':
    path = f'../logs/{name_logger}.log'

server_formatter = logging.Formatter('%(asctime)s %(levelname) -10s %(name)s %(filename)s %(message)s')

client_log_file = logging.FileHandler(path, encoding='utf-8')
client_log_file.setFormatter(server_formatter)

client_logger = logging.getLogger(name_logger)
client_logger.addHandler(client_log_file)
client_logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    client_logger.critical('АААА КРИТИЧНО!!!1')
    client_logger.error('Ошибка')
    client_logger.warning('Предупреждение!')
    client_logger.info('ИНФО')
    client_logger.debug('Отладка')
