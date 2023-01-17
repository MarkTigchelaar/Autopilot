
class UnlessStatement:
    def __init__(self):
        self.test_expression = None
        self.statements = None

    def add_expression(self, exp_ast):
        self.test_expression = exp_ast

    def add_statements(self, statements):
        self.statements = statements
