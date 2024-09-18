
class EnumStatement:
    def __init__(self):
        # Name will be replaced, but left in for now
        self.name = None
        self.name_token = None
        self.public_token = None
        # Same deal here
        self.item_list = list()
        self.items = self.item_list
        self.filled_in_items = list()
        self.general_type = None

    def add_name(self, name):
        self.name = name
        self.name_token = name

    def get_name(self):
        return self.name

    def add_public_token(self, public_token):
        self.public_token = public_token

    def add_general_type(self, type_token):
        self.general_type = type_token

    def get_general_type(self):
        return self.general_type

    def new_item(self, item_name_token, default_value_token):
        new_item = EnumListItem(item_name_token, default_value_token)
        self.item_list.append(new_item)
    
    def is_public(self):
        return self.public_token is not None

class EnumListItem:
    def __init__(self, item_name_token, default_value_token):
        self.item_name_token = item_name_token
        self.default_value_token = default_value_token

    def get_value(self):
        return self.default_value_token
