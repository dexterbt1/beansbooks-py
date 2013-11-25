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
        entity_search_data_key = "addresses"


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
    default_billing_address     = types.ReferenceField(CustomerAddress, via_key='default_billing_address_id')
    default_shipping_address    = types.ReferenceField(CustomerAddress, via_key='default_shipping_address_id')
    default_account             = types.ReferenceField(Account, via_key='default_account')
    sales_count                 = types.IntegerField(read_only=True)
    sales_total                 = types.DecimalField(read_only=True)
    balance_pending             = types.DecimalField(read_only=True)
    balance_pastdue             = types.DecimalField(read_only=True)

    class Meta:
        entity_url_path = "/Customer"
        entity_lookup_data_key = "customer"
        entity_search_data_key = "customers"



class CustomerSale(types.Entity):
    """
    https://beansbooks.com/api/explore/object/Customer/Sale
    """
    customer                    = types.ReferenceField(Customer, via_key='customer', required=True)
    account                     = types.ReferenceField(Account, via_key='account')
    sent                        = types.StringField() 
    refund_sale                 = types.ReferenceField('self', via_key='refund_sale_id')
    date_created                = types.StringField(required=True)
    date_billed                 = types.StringField()
    date_due                    = types.StringField()
    date_cancelled              = types.StringField()
    #create_transaction_id       = INTEGERThe ID for the Beans_Transaction tied to the sale creation.
    #invoice_transaction_id      = INTEGERThe ID for the Beans_Transaction tied to invoicing the sale.
    #cancel_transaction_id       = INTEGERThe ID for the Beans_Transaction tied to cancelling the sale.
    subtotal                    = types.DecimalField(read_only=True)
    total                       = types.DecimalField(read_only=True)
    taxestotal                  = types.DecimalField(read_only=True)
    balance                     = types.DecimalField(read_only=True)
    sale_number                 = types.StringField()
    order_number                = types.StringField()
    po_number                   = types.StringField()
    quote_number                = types.StringField()
    billing_address             = types.ReferenceField(CustomerAddress, via_key='billing_address')
    shipping_address            = types.ReferenceField(CustomerAddress, via_key='shipping_address')
    #lines                       = ARRAYAn array of Beans_Customer_Sale_Line.
    #taxes                       = ARRAYAn array of Beans_Customer_Sale_Tax - these are the applied taxes and their totals.
    #payments                    = ARRAYAn array of the Beans_Customer_Payment that this sale is tied to.
    status                      = types.StringField()
    title                       = types.StringField()
    
    class Meta:
        entity_url_path = "/Customer/Sale"
        entity_lookup_data_key = "sale"
        entity_search_data_key = "sales"



