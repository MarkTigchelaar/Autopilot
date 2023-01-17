


class AssignmentStatement:
    def __init__(self):
        self.let_or_var_token = None
        self.name_token = None
        self.type_token = None
        self.exp_ast = None
    
    def add_let_or_var(self, let_or_var_token):
        self.let_or_var_token = let_or_var_token

    def add_name(self, name_token):
        self.name_token = name_token

    def add_type(self, type_token):
        self.type_token = type_token

    def add_expression_value(self, exp_ast):
        self.exp_ast = exp_ast
    