from beansbooks.entities import types


class AccountType(types.Entity):
    """
    https://beansbooks.com/api/explore/object/Account/Type
    """
    name                    = types.StringField()
    code                    = types.StringField()
    type_short_code         = types.StringField()
    table_sign              = types.IntegerField()
    deposit                 = types.BooleanField()
    payment                 = types.BooleanField()
    receivable              = types.BooleanField()
    payable                 = types.BooleanField()
    reconcilable            = types.BooleanField()

    class Meta:
        entity_url_path = "/Account/Type"
        entity_lookup_data_key = "type"
        entity_search_data_key = "types"





class Account(types.Entity):
    """
    https://beansbooks.com/api/explore/object/Account
    """
    parent_account          = types.ReferenceField("self", via_key="parent_account_id")
    reserved                = types.BooleanField()
    name                    = types.StringField()
    code                    = types.StringField()
    balance                 = types.DecimalField(read_only=True)

    class Meta:
        entity_url_path = "/Account"
        entity_lookup_data_key = "account"
        entity_search_data_key = "accounts"

