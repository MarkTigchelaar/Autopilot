


class UnittestStatement:
    def __init__(self):
        self.statements = None
        self.name = None

    def add_test_name(self, name_token):
        self.name = name_token

    def get_name_token(self):
        return self.name

    def add_statements(self, statements):
        self.statements = statements

    def get_statements(self):
        return self.statements

    def accept(self, visitor):
        visitor.analyze_unittest_statements(self)
