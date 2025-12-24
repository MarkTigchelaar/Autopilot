


class ReturnStatement:
    def __init__(self):
        self.expression = None
        self.descriptor_token = None
    
    def add_expression(self, exp_ast):
        self.expression = exp_ast

    def has_expression_ast(self):
        return self.expression is not None

    def get_expression_ast(self):
        return self.expression

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token
    
    def has_nested_statements(self):
        return False
    
    def has_next_statement_in_block(self):
        return False
    
    def accept(self, visitor, scope_depth):
        visitor.analyze_return_statement(self, scope_depth)

    def accept_typesetter(self, visitor):
        if self.expression is not None:
            visitor.set_types(self.expression)

    def accept_resolved_function(self, type_annotater):
        return type_annotater.make_return_statement(self)