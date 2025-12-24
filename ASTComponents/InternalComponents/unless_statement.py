
class UnlessStatement:
    def __init__(self):
        self.test_expression = None
        self.statements = None
        self.descriptor_token = None

    def add_expression(self, exp_ast):
        self.test_expression = exp_ast

    def has_expression_ast(self):
        return self.test_expression is not None

    def get_expression_ast(self):
        return self.test_expression

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

    def accept_typesetter(self, visitor):
        visitor.set_types(self.test_expression)

    def accept_resolved_function(self, type_annotater):
        return type_annotater.make_unless_statement(self)