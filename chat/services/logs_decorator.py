import inspect
import logging
import sys


def log(func):
    def log_entry(*args, **kwargs):
        logger = logging.getLogger('server')
        if sys.argv[0].find('server') == -1:
            logger = logging.getLogger('client')

        logger.debug(
            f'функция: {func.__name__}, '
            f'с параметрами: {args}, {kwargs}, '
            f'вызвана из функции: {inspect.stack()[1][3]}.'
        )
        return func(*args, **kwargs)

    return log_entry
