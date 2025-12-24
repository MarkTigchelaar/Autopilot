class InterfaceStatement:
    def __init__(self):
        self.name_token = None
        self.fn_headers = None
        self.acyclic_token = None
        self.public_token = None

    def add_name(self, name_token):
        self.name_token = name_token

    def get_name(self):
        return self.name_token

    def add_function_headers(self, fn_headers):
        self.fn_headers = fn_headers

    def get_function_headers(self):
        return self.fn_headers

    def add_acyclic_token(self, acyclic_token):
        self.acyclic_token = acyclic_token

    def add_public_token(self, public_token):
        self.public_token = public_token

    def is_public(self):
        return self.public_token is not None
