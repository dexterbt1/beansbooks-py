*************
beansbooks-py
*************

Python Client library for interacting with the `BeansBooks <https://github.com/system76/beansbooks>` REST API.

BeansBooks is an up-and-coming, open-source, web-based accounting system for small/medium organizations. 
We wrote this client library to help us integrate and automate tasks in our BeansBooks instance. 
We needed things like an automated creation of invoices (for recurring billing / subscriptions), 
sync data between our SaaS system and BB, overdue invoice reminders, etc.; all via leveraging the use of 
the REST API.


Sample Usage
------------

A rich, ORM-like DSL is provided for easy programmatic access to the entities / objects of the 
BeansBooks system.

To illustrate usage, see the sample client code below::

    from beansbooks.api.v1 import Client, AuthAccess
    from beansbooks.api.v1 import request
    from beansbooks.entities import Customer

    auth = AuthAccess(
                uid='xxxxx...',
                expiration='yyyyy..',
                key='zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz....',
                )
    client = Client('http://my.beansbooks.host/api', auth=auth)

    customer = client.execute(request.Lookup(Customer, 1))
    print customer.id
    print customer.first_name
    print customer.last_name

    
References
----------

- `Source Code <http://github.com/dexterbt1/beansbooks-py>`_
- Feedback / Patches - `Create an issue <http://github.com/dexterbt1/beansbooks-py/issues>`_


Copyright © 2013, Dexter B. Tad-y

