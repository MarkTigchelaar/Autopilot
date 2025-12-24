
class EnumStatement:
    def __init__(self):
        # Name will be replaced, but left in for now
        self.name_token = None
        self.public_token = None
        # Same deal here
        self.item_list = list()
        self.general_type = None
        self.value_type_ref = None

    def set_value_type_ref(self, type_ref):
        self.value_type_ref = type_ref

    def all_items_have_types(self) -> bool:
        return self.value_type_ref is not None

    def add_name(self, name):
        self.name_token = name

    def get_name(self):
        return self.name_token
    
    def get_items(self):
        return self.item_list

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
    
    def set_default_value(self, default_value_token):
        self.default_value_token = default_value_token
    
    def get_name(self):
        return self.item_name_token
