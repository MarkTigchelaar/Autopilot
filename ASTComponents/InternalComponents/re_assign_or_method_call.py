


class ReassignmentOrMethodCall:
    def __init__(self):
        self.l_value_exp = None
        self.assignment_token = None
        self.r_value_exp = None
        self.descriptor_token = None
    
    def add_l_value_exp(self, l_value_exp):
        self.l_value_exp = l_value_exp

    def add_assignment_token(self, assignment_token):
        self.assignment_token = assignment_token
    
    def get_assignment_token(self):
        return self.assignment_token

    def add_r_value(self, r_value_exp):
        self.r_value_exp = r_value_exp

    
    def get_l_value(self):
        return self.l_value_exp
    
    def is_reassignment(self):
        return self.assignment_token is not None

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token

    def has_nested_statements(self):
        return False
    
    def has_next_statement_in_block(self):
        return False
    
    def accept(self, visitor, scope_depth):
        visitor.analyze_re_assign_or_method_call(self, scope_depth)

    def accept_typesetter(self, visitor):
        visitor.set_types(self.r_value_exp)
        visitor.set_types(self.l_value_exp)
    
    def accept_resolved_function(self, type_annotater):
        if self.is_reassignment():
            return type_annotater.make_reassignment_statement(self)
        return type_annotater.make_method_call_statement(self)