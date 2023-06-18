
class ElseStatement:
    def __init__(self):
        self.statements = None
        self.descriptor_token = None
        self.next_statement_in_block = None


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