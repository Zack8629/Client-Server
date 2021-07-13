import unittest

from client_1 import handle_response, create_presence_message
from services.commands import get_configs


class TestClient(unittest.TestCase):
    config = get_configs('client', is_server=False)

    def test_create_presence_message(self):
        test_create_presence_message = create_presence_message('Guest')
        test_create_presence_message[self.config['TIME']] = 1.1
        self.assertEqual(
            test_create_presence_message,
            {
                self.config['ACTION']: self.config.get('PRESENCE'),
                self.config['TIME']: 1.1,
                self.config['USER']: {
                    self.config['ACCOUNT_NAME']: 'Guest'
                }
            }
        )

    def test_response_200(self):
        self.assertEqual(
            handle_response({self.config['RESPONSE']: 200}),
            '200 : OK'
        )

    def test_response_400(self):
        self.assertEqual(
            handle_response({self.config['RESPONSE']: 400,
                             self.config['ERROR']: 'Bad Request'}),
            '400 : Bad Request'
        )


if __name__ == '__main__':
    unittest.main()
