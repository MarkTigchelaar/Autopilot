

class MethodCallOrFieldExpression:
    def __init__(self):
        self.struct_name_exp = None
        self.argument_list = None

    def add_lhs_exp(self, left_exp):
        self.struct_name_exp = left_exp
    
    def add_field_or_methods(self, field_or_method_list):
        self.argument_list = field_or_method_list

    def accept(self, expression_analyzer):
        expression_analyzer.visit_method_call_or_field_expression(self)

    def has_left_expression(self):
        return True
    
    def has_right_expression(self): 
        return False
