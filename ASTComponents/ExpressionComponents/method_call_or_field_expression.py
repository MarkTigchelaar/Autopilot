class MethodCallOrFieldExpression:
    def __init__(self):
        self.struct_name_exp = None
        self.argument_list = None

    def add_lhs_exp(self, left_exp):
        self.struct_name_exp = left_exp
    
    def get_lhs_exp(self):
        return self.struct_name_exp
    
    def set_type(self, _type):
        if len(self.argument_list) > 0:
            return self.argument_list[-1].set_type(_type)
        self.struct_name_exp.set_type(_type)

    def get_type(self):
        if len(self.argument_list) > 0:
            return self.argument_list[-1].get_type()
        return self.struct_name_exp.get_type()
    
    def add_field_or_methods(self, field_or_method_list):
        self.argument_list = field_or_method_list

    def get_field_or_methods(self):
        return self.argument_list
    
    def has_fields_and_methods(self):
        return self.argument_list is not None and len(self.argument_list) > 0

    # def accept(self, expression_analyzer):
    #     expression_analyzer.analyze_field_or_method_chain_expression(self)

    def has_left_expression(self):
        return True
    
    def has_right_expression(self): 
        return False
    
    def accept_resolved_statement(self, type_annotater):
        return type_annotater.make_method_call_or_field_expression(self)