import unittest
import decimal

from beansbooks.entities.types import StringField, IntegerField, DecimalField

class BuiltinTypesTest1(unittest.TestCase):

    def test_string1(self):
        f = StringField()
        self.assertTrue(hasattr(f,'from_remote'))
        self.assertTrue(hasattr(f,'to_remote'))

        raw_inp = 'Hello World'
        inp = f.from_remote(None, raw_inp)
        self.assertEquals(inp, 'Hello World')
        self.assertTrue(isinstance(inp, basestring))

    def test_int1(self):
        f = IntegerField()
        self.assertTrue(hasattr(f,'from_remote'))
        self.assertTrue(hasattr(f,'to_remote'))
    
        raw_inp = int(1231)
        inp = f.from_remote(None, raw_inp)
        self.assertEquals(inp, 1231)
        self.assertTrue(isinstance(inp, int))

    def test_decimal1(self):
        f = DecimalField()
        self.assertTrue(hasattr(f,'from_remote'))
        self.assertTrue(hasattr(f,'to_remote'))
    
        raw_inp = "12.34"
        inp = f.from_remote(None, raw_inp)
        self.assertEquals(inp, decimal.Decimal('12.34'))
        self.assertTrue(isinstance(inp, decimal.Decimal))


