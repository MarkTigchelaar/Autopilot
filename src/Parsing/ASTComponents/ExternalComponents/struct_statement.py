

class StructStatement:
    def __init__(self):
        self.acyclic_token = None
        self.inline_token = None
        self.public_token = None
        self.name_token = None
        self.fields = list()
        self.functions = list()
        self.interfaces = list()

    def add_name(self, name_token):
        self.name_token = name_token

    def add_acyclic_token(self, acyclic_token):
        self.acyclic_token = acyclic_token

    def add_public_token(self, public_token):
        self.public_token = public_token

    def add_inline_token(self, inline_token):
        self.inline_token = inline_token
    
    def add_field(self, field):
        self.fields.append(field)

    def add_function(self, function):
        self.functions.append(function)
    
    def add_interface(self, interface_token):
        self.interfaces.append(interface_token)


class StructField:
    def __init__(self):
        self.public_token = None
        #self.acyclic_token = None
        #self.inline_token = None
        self.field_name_token = None
        self.type_token = None

    def add_public_token(self, public_token):
        self.public_token = public_token
    
    # def add_acyclic_token(self, acyclic_token):
    #     self.acyclic_token = acyclic_token
    
    # def add_inline_token(self, inline_token):
    #     self.inline_token = inline_token
    
    def add_field_name(self, field_name_token):
        self.field_name_token = field_name_token
    
    def add_type_token(self, type_token):
        self.type_token = type_token
