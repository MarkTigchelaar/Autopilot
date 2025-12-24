class ModuleStatement:
    def __init__(self):
        self.name = None

    def add_name(self, name_token):
        self.name = name_token

    def get_name(self):
        return self.name

    def is_public(self):
        return False
