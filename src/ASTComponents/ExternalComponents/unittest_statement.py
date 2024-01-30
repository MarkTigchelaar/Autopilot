


class UnittestStatement:
    def __init__(self):
        self.statements = None
        self.name = None

    def add_test_name(self, name_token):
        self.name = name_token

    def add_statements(self, statements):
        self.statements = statements
