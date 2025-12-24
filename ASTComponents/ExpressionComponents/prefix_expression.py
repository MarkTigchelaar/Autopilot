from Tokenization.token import Token

class PrefixExpression:
    def __init__(self):
        self.token: Token = None
        self.rhs_exp = None
        self.data_type = None

    def add_name(self, token):
        self.token = token

    def get_name(self):
        return self.token

    def add_rhs_exp(self, rhs_expression):
        self.rhs_exp = rhs_expression

    def get_rhs_exp(self):
        return self.rhs_exp
    
    def set_type(self, _type):
        self.data_type = _type

    def get_type(self):
        return self.data_type

    # def accept(self, expression_analyzer):
    #     expression_analyzer.analyze_prefix_expression(self)

    def has_left_expression(self):
        return False
    
    def has_right_expression(self):
        return self.rhs_exp is not None

    def accept_resolved_statement(self, type_annotater):
        return type_annotater.make_prefix_expression(self)