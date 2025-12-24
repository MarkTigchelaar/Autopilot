class FunctionStatement:
    def __init__(self):
        self.header = None
        self.statements = None
        self.acyclic_token = None
        self.inline_token = None
        self.pub_token = None

    def add_header(self, header):
        self.header = header

    def get_header(self):
        return self.header

    def get_return_type_actual_reference(self):
        return self.header.get_return_type_actual_reference()
    
    def get_name_token(self):
        return self.header.get_name()
    
    def get_name(self):
        return self.get_name_token()
    
    def add_statements(self, statements):
        self.statements = statements

    def get_statements(self):
        return self.statements
    
    def get_args(self):
        return self.header.get_args()
    
    def has_arguments(self):
        return len(self.get_args()) > 0
    
    def get_return_type(self):
        return self.header.get_return_type()
    
    def add_acyclic_token(self, acyclic_token):
        self.acyclic_token = acyclic_token

    def add_inline_token(self, inline_token):
        self.inline_token = inline_token

    def get_inline_token(self):
        return self.inline_token
    
    def add_public_token(self, pub_token):
        self.pub_token = pub_token

    def is_public(self):
        return self.pub_token is not None

    def accept(self, visitor):
        visitor.analyze_function_statements(self)

