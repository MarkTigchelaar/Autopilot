


class PrefixExpression:
    def __init__(self):
        self.token = None
        self.rhs_exp = None

    def add_name(self, token):
        self.token = token

    def add_rhs_exp(self, rhs_expression):
        self.rhs_exp = rhs_expression
    