

class MethodCallOrFieldExpression:
    def __init__(self):
        self.struct_name_exp = None
        self.argument_list = None

    def add_lhs_exp(self, left_exp):
        self.struct_name_exp = left_exp
    
    def add_field_or_methods(self, field_or_method_list):
        self.argument_list = field_or_method_list
