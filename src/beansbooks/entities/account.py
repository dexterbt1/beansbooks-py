from beansbooks.entities import types

class Account(types.Entity):
    """
    https://beansbooks.com/api/explore/object/Object
    """
    name                    = types.StringField()
    code                    = types.StringField()
    balance                 = types.DecimalField(read_only=True)

    class Meta:
        entity_url_path = "/Account"
        entity_lookup_data_key = "account"

