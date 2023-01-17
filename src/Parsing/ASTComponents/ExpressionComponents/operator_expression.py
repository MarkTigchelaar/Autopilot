

class OperatorExpression:
    def __init__(self):
        self.operator_token = None
        self.left_expression = None
        self.right_expression = None

    def add_name(self, operator_token):
        self.operator_token = operator_token
    
    def add_lhs_exp(self, lhs_exp):
        self.left_expression = lhs_exp
    
    def add_rhs_exp(self, rhs_exp):
        self.right_expression = rhs_exp
