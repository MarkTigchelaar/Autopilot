#from ASTComponents.InternalComponents.re_assign_or_method_call import ReassignmentOrMethodCall

class DeferStatement:
    def __init__(self):
        self.method_call = None
        self.descriptor_token = None
    
    def add_reassignment_statement(self, re_assign_stmt):
        self.method_call = re_assign_stmt

    def add_descriptor_token(self, token):
        self.descriptor_token = token
    
    def get_method_or_reassignment(self):
        return self.method_call

    def get_descriptor_token(self):
        return self.descriptor_token
    
    def has_nested_statements(self):
        return False
    
    def has_next_statement_in_block(self):
        return False
    
    def accept(self, visitor, scope_depth):
        visitor.analyze_defer_statement(self, scope_depth)
