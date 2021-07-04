import unittest

from commands import get_configs
from server import handle_message


class TestServer(unittest.TestCase):
    config = get_configs()

    def test_response_200(self):
        message = {
            self.config['ACTION']: self.config.get('PRESENCE'),
            self.config['TIME']: '1.1',
            self.config['USER']: {
                self.config['ACCOUNT_NAME']: 'Guest'
            }
        }

        self.assertEqual(handle_message(message),
                         {self.config['RESPONSE']: 200},
                         'test_response_200')

    def test_response_400(self):
        message = {
            self.config['ACTION']: self.config.get('PRESENCE'),
            self.config['TIME']: '1.1',
        }

        self.assertEqual(handle_message(message),
                         {self.config['RESPONSE']: 400,
                          self.config['ERROR']: 'Bad Request'},
                         'test_response_400')


if __name__ == '__main__':
    unittest.main()
