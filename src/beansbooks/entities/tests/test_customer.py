import unittest

from beansbooks.entities.customer import Customer

class CustomerTests1(unittest.TestCase):

    def test_init_ok1(self):
        c = Customer(
                first_name='John',
                last_name='Doe',
                company_name='XYZ Corp.',
                email='johndoe@xyzcorp.co',
                phone_number='1234-5678-90',
                fax_number='',
                )
        self.assertEquals(c.first_name, 'John')
        self.assertEquals(c.last_name, 'Doe')
        self.assertEquals(c.company_name, 'XYZ Corp.')
        self.assertEquals(c.email, 'johndoe@xyzcorp.co')
        self.assertEquals(c.phone_number, '1234-5678-90')
        self.assertEquals(c.fax_number, '')

    def test_init_required(self):
        self.assertRaises(ValueError, Customer)
        self.assertRaises(ValueError, Customer, first_name='John')
        try:
            Customer(first_name='John', last_name='Doe')
        except:
            self.fail("Required fields should be ok but exception raised")


    def test_init_readonly(self):
        self.assertRaises(ValueError, Customer, first_name='John', last_name='Doe', sales_count=123)
        
