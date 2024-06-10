

class OperatorExpression:
    def __init__(self):
        self.operator_token = None
        self.left_expression = None
        self.right_expression = None

    def add_name(self, operator_token):
        self.operator_token = operator_token

    def get_name(self):
        return self.operator_token
    
    def add_lhs_exp(self, lhs_exp):
        self.left_expression = lhs_exp

    def get_lhs_exp(self):
        return self.left_expression
    
    def add_rhs_exp(self, rhs_exp):
        self.right_expression = rhs_exp

    def get_rhs_exp(self):
        return self.right_expression

    def accept(self, expression_analyzer):
        expression_analyzer.visit_binary_operator_expression(self)
