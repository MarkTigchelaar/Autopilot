
class ContinueStatement:
    def __init__(self):
        self.descriptor_token = None

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token

    def has_nested_statements(self):
        return False

    def has_next_statement_in_block(self):
        return False
    
    def accept(self, visitor, scope_depth):
        visitor.analyze_continue_statement(self, scope_depth)
