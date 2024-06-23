


class PrefixExpression:
    def __init__(self):
        self.token = None
        self.rhs_exp = None

    def add_name(self, token):
        self.token = token

    def get_name(self):
        return self.token

    def add_rhs_exp(self, rhs_expression):
        self.rhs_exp = rhs_expression

    def get_rhs_exp(self):
        return self.rhs_exp

    def accept(self, expression_analyzer):
        expression_analyzer.visit_prefix_expression(self)

    def has_left_expression(self):
        return False
    
    def has_right_expression(self):
        return self.rhs_exp is not None
