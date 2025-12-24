
class FunctionHeaderStatement:
    def __init__(self):
        self.name_token = None
        self.arguments = list()
        self.return_type_token = None
        self.acyclic_token = None
        self.is_public = False
        self.inline_token = None
        self.public_token = None
        self.return_type_actual_reference = None

    def add_name(self, name_token):
        self.name_token = name_token
    
    def get_name(self):
        return self.name_token

    def add_arg(self, argument):
        self.arguments.append(argument)

    def get_args(self):
        return self.arguments
    
    def add_return_type(self, return_type_token):
        self.return_type_token = return_type_token

    def get_return_type(self):
        return self.return_type_token
    
    def add_return_type_actual_reference(self, actual_reference):
        self.return_type_actual_reference = actual_reference
    
    def get_return_type_actual_reference(self):
        return self.return_type_actual_reference
    

    def add_acyclic_field(self, acyclic_token):
        self.acyclic_token = acyclic_token

    def set_as_public(self, is_public):
        self.is_public = is_public
    
    def is_public(self):
        return self.is_public

    def add_inline_token(self, inline_token):
        self.inline_token = inline_token
    
    def add_public_token(self, public_token):
        self.public_token = public_token

    def add_acyclic_token(self, acyclic_token):
        self.acyclic_token = acyclic_token

class FunctionArgument:
    def __init__(self):
        self.arg_name_token = None
        self.arg_type_token = None
        self.default_value_token = None
        self.actual_type_reference = None

    def add_name(self, arg_name_token):
        self.arg_name_token = arg_name_token
    
    def get_name(self):
        return self.arg_name_token

    def add_type(self, arg_type_token):
        self.arg_type_token = arg_type_token

    def get_type(self):
        return self.arg_type_token
    
    def add_default_value(self, default_value_token):
        self.default_value_token = default_value_token

    def get_default_value(self):
        return self.default_value_token
    
    def set_value_type_ref(self, actual_type_reference):
        self.actual_type_reference = actual_type_reference
