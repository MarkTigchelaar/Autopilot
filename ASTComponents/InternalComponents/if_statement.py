from Tokenization.symbols import LET

class IfStatement:
    def __init__(self):
        self.test_expression = None
        self.optional_assignment_type = None
        self.unwrapped_optional_variable_name = None
        self.optional_variable_name = None
        self.statements = None
        self.next_statement_in_block = None
        self.descriptor_token = None

    def is_option_type(self):
        # let | var
        return self.optional_assignment_type is not None
    
    def is_let_var_type(self):
        if not self.is_option_type():
            return False
        return self.get_assignment_type().internal_type == LET

    def add_expression(self, exp_ast):
        self.test_expression = exp_ast
    
    def get_expression_ast(self):
        return self.test_expression
    
    def has_expression_ast(self):
        return self.test_expression is not None

    def add_assignment_type(self, assign_type_token):
        self.optional_assignment_type = assign_type_token
    
    def get_assignment_type(self):
        return self.optional_assignment_type

    def add_variable_name(self, variable_token):
        self.unwrapped_optional_variable_name = variable_token

    def get_variable_name(self):
        return self.unwrapped_optional_variable_name

    def add_optional_name(self, option_name_token):
        self.optional_variable_name = option_name_token
    
    def get_optional_name(self):
        return self.optional_variable_name

    def add_statements(self, statements):
        self.statements = statements
    
    def get_statements(self):
        return self.statements

    def add_next_statement_in_block(self, statement):
        self.next_statement_in_block = statement

    def get_next_statement_in_block(self):
        return self.next_statement_in_block

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token
    
    def has_nested_statements(self):
        return True
    
    def has_next_statement_in_block(self):
        return self.next_statement_in_block is not None
    
    def accept(self, visitor, scope_depth):
        visitor.analyze_if_statement(self, scope_depth)

    def accept_typesetter(self, visitor):
        if self.has_expression_ast():
            visitor.set_types(self.test_expression)
        if self.is_option_type():
            visitor.set_type_on_variable(self.optional_variable_name)


    def accept_resolved_function(self, type_annotater):
        return type_annotater.make_if_statement(self)