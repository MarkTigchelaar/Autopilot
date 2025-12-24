
class UnionStatement:
    def __init__(self):
        self.name_token = None
        self.public_token = None
        self.items = list()
    
    def add_name(self, name_token):
        self.name_token = name_token

    def get_name(self):
        return self.name_token

    def add_public_token(self, public_token):
        self.public_token = public_token

    def add_item(self, item_name_token, type_token):
        item = UnionListItem(item_name_token, type_token)
        self.items.append(item)

    def get_fields(self):
        return self.items

    def is_public(self):
        return self.public_token is not None


class UnionListItem:
    def __init__(self, item_name_token, type_token):
        self.item_name_token = item_name_token
        self.type_token = type_token
        self.value_type_ref = None

    def get_value(self):
        return self.type_token
    
    def get_type(self):
        return self.type_token
    
    def set_value_type_ref(self, type_ref):
        self.value_type_ref = type_ref
