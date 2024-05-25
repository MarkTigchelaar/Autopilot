

class LoopStatement:
    def __init__(self):
        self.loop_name = None
        self.statements = None
        self.descriptor_token = None

    def add_loop_name(self, loop_name):
        self.loop_name = loop_name

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
        visitor.analyze_loop_statement(self, scope_depth)
