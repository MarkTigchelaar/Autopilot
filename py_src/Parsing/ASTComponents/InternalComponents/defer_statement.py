#from Parsing.ASTComponents.InternalComponents.re_assign_or_method_call import ReassignmentOrMethodCall

class DeferStatement:
    def __init__(self):
        self.method_call = None
    
    def add_reassignment_statement(self, re_assign_stmt):
        self.method_call = re_assign_stmt
