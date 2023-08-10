
class EnumStatement:
    def __init__(self):
        self.name = None
        self.public_token = None
        self.item_list = list()
        self.general_type = None

    def add_name(self, name):
        self.name = name

    def add_public_token(self, public_token):
        self.public_token = public_token

    def add_general_type(self, type_token):
        self.general_type = type_token

    def new_item(self, item_name_token, default_value_token):
        new_item = EnumListItem(item_name_token, default_value_token)
        self.item_list.append(new_item)

class EnumListItem:
    def __init__(self, item_name_token, default_value_token):
        self.item_name_token = item_name_token
        self.default_value_token = default_value_token
