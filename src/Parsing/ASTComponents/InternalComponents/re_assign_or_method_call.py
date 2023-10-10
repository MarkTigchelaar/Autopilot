


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

    def add_r_value(self, r_value_exp):
        self.r_value_exp = r_value_exp

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token

    def has_nested_statements(self):
        return False
    
    def has_next_statement_in_block(self):
        return False