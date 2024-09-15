
class FunctionCallExpression:
    def __init__(self):
        self.fn_name_exp = None
        self.argument_list = None

    def add_name_exp(self, fn_name_exp):
        self.fn_name_exp = fn_name_exp
    
    def get_name(self):
        return self.fn_name_exp

    def add_argument_list(self, argument_list):
        self.argument_list = argument_list

    def get_argument_list(self):
        return self.argument_list

    def accept(self, expression_analyzer):
        expression_analyzer.visit_function_call_expression(self)

    def has_left_expression(self):
        return False
    
    def has_right_expression(self): 
        return False
