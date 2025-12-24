from Tokenization.symbols import LET

# Should be renamed to DeclarationStatement
class AssignmentStatement:
    def __init__(self):
        self.let_or_var_token = None
        self.name_token = None
        self.type_token = None
        self.exp_ast = None
        self.descriptor_token = None
        # A shoe horn
        self.been_analyzed = False
    
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
    
    def is_let_type_variable(self):
        return self.descriptor_token.internal_type == LET

    def has_nested_statements(self):
        return False

    def has_next_statement_in_block(self):
        return False
    
    def accept(self, visitor, scope_depth):
        if not self.been_analyzed:
            self.been_analyzed = True
            visitor.analyze_declaration(self, scope_depth)

    def accept_typesetter(self, visitor):
        visitor.set_types(self.exp_ast)


    def accept_resolved_function(self, type_annotater):
        return type_annotater.make_assignment_statement(self)