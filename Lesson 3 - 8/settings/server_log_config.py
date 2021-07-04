import logging

name_logger = 'server'
path = f'logs/{name_logger}.log'

if __name__ == '__main__':
    path = f'../logs/{name_logger}.log'

server_formatter = logging.Formatter('%(asctime)s %(levelname) -10s %(name)s %(filename)s %(message)s')

server_log_file = logging.FileHandler(path, encoding='utf-8')
server_log_file.setFormatter(server_formatter)

server_logger = logging.getLogger(name_logger)
server_logger.addHandler(server_log_file)
server_logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    server_logger.critical('АААА КРИТИЧНО!!!1')
    server_logger.error('Ошибка')
    server_logger.warning('Предупреждение!')
    server_logger.info('ИНФО')
    server_logger.debug('Отладка')
