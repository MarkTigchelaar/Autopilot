
class ErrorStatement:
    def __init__(self):
        self.name_token = None
        self.public_token = None
        self.items = list()

    def add_name(self, name_token):
        self.name_token = name_token

    def add_public_token(self, public_token):
        self.public_token = public_token

    def new_item(self, item_name_token):
        self.items.append(item_name_token)
