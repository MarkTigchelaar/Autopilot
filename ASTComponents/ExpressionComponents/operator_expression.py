

class OperatorExpression:
    def __init__(self):
        self.token = None
        self.left_expression = None
        self.right_expression = None
        self.type = None

    def add_name(self, token):
        self.token = token

    def get_name(self):
        return self.token
    
    def set_type(self, _type):
        self.type = _type

    def get_type(self):
        return self.type
    
    def add_lhs_exp(self, lhs_exp):
        self.left_expression = lhs_exp

    def get_lhs_exp(self):
        return self.left_expression
    
    def add_rhs_exp(self, rhs_exp):
        self.right_expression = rhs_exp

    def get_rhs_exp(self):
        return self.right_expression

    # def accept(self, expression_analyzer):
    #     expression_analyzer.analyze_binary_expression(self)

    def has_left_expression(self):
        return self.left_expression is not None

    def has_right_expression(self): 
        return self.right_expression is not None

    def accept_resolved_statement(self, type_annotater):
        return type_annotater.make_operator_expression(self)