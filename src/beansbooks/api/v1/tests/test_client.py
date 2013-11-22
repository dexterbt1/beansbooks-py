import unittest
from beansbooks.api.v1 import Client, AuthAccess


class ClientTest1(unittest.TestCase):

    def test_init(self):
        c = Client('http://localhost/api')
        self.assertTrue(type(c) == Client)

    def test_init_auth(self):
        c = Client('http://localhost/api', auth=AuthAccess(uid='uidhere', key='keyhere', expiration='exphere'))
        self.assertTrue(type(c) == Client)
        self.assertTrue(c.auth.uid == 'uidhere')
        self.assertTrue(c.auth.key == 'keyhere')
        self.assertTrue(c.auth.expiration == 'exphere')


