import unittest

from beansbooks.entities.customer import Customer
from beansbooks.api.v1 import request


class RequestTest1(unittest.TestCase):

    def test_lookup1(self):
        q = request.Lookup(Customer, 1)
        self.assertTrue(hasattr(q, 'headers'))
        self.assertTrue(hasattr(q, 'content'))
        self.assertEquals(q.content, 
            { 'id': 1 },
            )


