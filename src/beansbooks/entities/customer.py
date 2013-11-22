from beansbooks.entities import types
#from beansbooks.entities.account import Account

#class CustomerAddress(types.Entity):

class Customer(types.Entity):
    """
    https://beansbooks.com/api/explore/object/Customer
    """

    first_name                  = types.String(required=True)
    last_name                   = types.String(required=True)
    company_name                = types.String()
    email                       = types.String()
    phone_number                = types.String()
    fax_number                  = types.String()
    #default_billing_address     = types.Reference(to=CustomerAddress)
    #default_shipping_address    = types.Reference(to=CustomerAddress)
    #default_account             = types.Reference(to=Account)
    sales_count                 = types.Integer(read_only=True)
    sales_total                 = types.Decimal(read_only=True)
    balance_pending             = types.Decimal(read_only=True)
    balance_pastdue             = types.Decimal(read_only=True)

    class Meta:
        entity_name = "Customer"
        entity_response_data_key = "customer"
