

# Should be renamed to DeclarationStatement
class AssignmentStatement:
    def __init__(self):
        self.let_or_var_token = None
        self.name_token = None
        self.type_token = None
        self.exp_ast = None
        self.descriptor_token = None
    
    def add_let_or_var(self, let_or_var_token):
        self.let_or_var_token = let_or_var_token
        self.add_descriptor_token(let_or_var_token)

    def add_name(self, name_token):
        self.name_token = name_token

    def get_name(self):
        return self.name_token

    def add_type(self, type_token):
        self.type_token = type_token

    def get_type(self):
        return self.type_token

    def add_expression_value(self, exp_ast):
        self.exp_ast = exp_ast

    def get_expression_ast(self):
        return self.exp_ast

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token

    def has_nested_statements(self):
        return False

    def has_next_statement_in_block(self):
        return False
    
    def accept(self, visitor, scope_depth):
        visitor.analyze_declaration(self, scope_depth)
