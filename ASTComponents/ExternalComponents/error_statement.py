
class ErrorStatement:
    def __init__(self):
        self.name_token = None
        self.public_token = None
        self.items = list()
        self.value_type_ref = None

    def set_value_type_ref(self, type_ref):
        self.value_type_ref = type_ref

    def all_items_have_types(self) -> bool:
        return self.value_type_ref is not None

    def add_name(self, name_token):
        self.name_token = name_token

    def get_name(self):
        return self.name_token

    def add_public_token(self, public_token):
        self.public_token = public_token

    def new_item(self, item_name_token):
        self.items.append(item_name_token)

    def is_public(self):
        return self.public_token is not None