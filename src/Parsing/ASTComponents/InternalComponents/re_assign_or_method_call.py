


class ReassignmentOrMethodCall:
    def __init__(self):
        self.l_value_exp = None
        self.assignment_token = None
        self.r_value_exp = None
    
    def add_l_value_exp(self, l_value_exp):
        self.l_value_exp = l_value_exp

    def add_assignment_token(self, assignment_token):
        self.assignment_token = assignment_token

    def add_r_value(self, r_value_exp):
        self.r_value_exp = r_value_exp
