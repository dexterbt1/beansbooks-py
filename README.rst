*************
beansbooks-py
*************

Python Client library for writing python programs that integrate with the BeansBooks `REST API <https://beansbooks.com/api>`_.

`BeansBooks <https://github.com/system76/beansbooks>`_ is an open-source, web-based accounting system for small/medium organizations. 

We wrote this client library because we needed things like an automated creation of invoices (for recurring billing / subscriptions), 
synchronize/validate data between our custom applications and BeansBooks, issue overdue invoice reminders, etc.; all leveraging the use of 
the REST API.


Sample Usage
------------

An ORM-like DSL is provided for easy programmatic access to the entities / objects of the 
BeansBooks system.

To illustrate usage, see the sample client code below::

    from beansbooks.api.v1 import Client, AuthAccess
    from beansbooks.api.v1 import request
    from beansbooks.entities.customer import Customer

    auth = AuthAccess(uid='xx...', expiration='yy...', key='zz...')
    client = Client('http://my.beansbooks.host/api', auth=auth)

    # lookup - returns one object
    customer = client.execute(request.Lookup(Customer, 1))

    print customer.id
    print customer.first_name
    print customer.last_name

    # automatically fetch the related objects
    billing_address = customer.default_billing_address
    print billing_address.standard

    # create
    johndoe = Customer(first_name='John', last_name='Doe')
    client.execute(request.Create(johndoe))
    print johndoe.id


    
References
----------

- `Source Code <http://github.com/dexterbt1/beansbooks-py>`_
- `BeansBook Home Page <https://beansbooks.com/>`_
- `BeansBook REST API <http://beansbooks.com/api>`_
- Feedback / Patches - `Create an issue <http://github.com/dexterbt1/beansbooks-py/issues>`_



Copyright © 2013, Dexter B. Tad-y

