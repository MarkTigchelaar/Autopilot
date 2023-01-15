

class WhileStatement:
    def __init__(self):
        self.test_expression = None
        self.loop_name = None
        self.statements = None

    def add_expression(self, exp_ast):
        self.test_expression = exp_ast

    def add_loop_name(self, loop_name):
        self.loop_name = loop_name

    def add_statements(self, statements):
        self.statements = statements
