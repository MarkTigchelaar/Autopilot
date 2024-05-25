
class UnlessStatement:
    def __init__(self):
        self.test_expression = None
        self.statements = None
        self.descriptor_token = None

    def add_expression(self, exp_ast):
        self.test_expression = exp_ast

    def add_statements(self, statements):
        self.statements = statements

    def get_statements(self):
        return self.statements

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token
    
    def has_nested_statements(self):
        return True
    
    def has_next_statement_in_block(self):
        return False
    
    def accept(self, visitor, scope_depth):
        visitor.analyze_unless_statement(self, scope_depth)
