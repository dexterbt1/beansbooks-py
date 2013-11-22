from beansbooks.entities import types
from beansbooks.entities.account import Account

class CustomerAddress(types.Entity):
    """
    https://beansbooks.com/api/explore/object/Customer/Address
    """
    first_name                  = types.StringField()
    last_name                   = types.StringField()
    company_name                = types.StringField()
    address1                    = types.StringField()
    address2                    = types.StringField()
    city                        = types.StringField()
    state                       = types.StringField()
    zip                         = types.StringField()
    country                     = types.StringField()
    standard                    = types.StringField()

    class Meta:
        entity_url_path = "/Customer/Address"
        entity_lookup_data_key = "address"


class Customer(types.Entity):
    """
    https://beansbooks.com/api/explore/object/Customer
    """
    first_name                  = types.StringField(required=True)
    last_name                   = types.StringField(required=True)
    company_name                = types.StringField()
    email                       = types.StringField()
    phone_number                = types.StringField()
    fax_number                  = types.StringField()
    default_billing_address     = types.ReferenceField(to=CustomerAddress, via_key='default_billing_address_id')
    default_shipping_address    = types.ReferenceField(to=CustomerAddress, via_key='default_shipping_address_id')
    default_account             = types.ReferenceField(to=Account, via_key='default_account')
    sales_count                 = types.IntegerField(read_only=True)
    sales_total                 = types.DecimalField(read_only=True)
    balance_pending             = types.DecimalField(read_only=True)
    balance_pastdue             = types.DecimalField(read_only=True)

    class Meta:
        entity_url_path = "/Customer"
        entity_lookup_data_key = "customer"
