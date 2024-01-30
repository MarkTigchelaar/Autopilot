
class FunctionCallExpression:
    def __init__(self):
        self.fn_name_exp = None
        self.argument_list = None

    def add_name_exp(self, fn_name_exp):
        self.fn_name_exp = fn_name_exp

    def add_argument_list(self, argument_list):
        self.argument_list = argument_list
