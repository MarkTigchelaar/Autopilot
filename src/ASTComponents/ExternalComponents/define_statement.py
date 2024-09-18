
class DefineStatement:
    def __init__(self):
        self.sub_type = None
        self.new_type_name_token = None
        self.descriptor_token = None

    def add_subtype(self, sub_type):
        self.sub_type = sub_type

    def add_definition(self, definition_token):
        self.new_type_name_token = definition_token

    def get_definition(self):
        return self.new_type_name_token

    def get_key_token(self):
        return self.sub_type.get_key_token()
    
    def get_value_token(self):
        return self.sub_type.get_value_token()
    
    def get_arg_list(self):
        return self.sub_type.get_arg_list()
    
    def get_error_token(self):
        return self.sub_type.get_error_token()

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token
    
    def is_public(self):
        return False


# HashMaps, Dictionarys, Map interface
class KeyValueType:
    def __init__(self):
        self.type_token = None
        self.key_token = None
        self.value_token = None
        self.descriptor_token = None

    def add_type_token(self, type_token):
        self.type_token = type_token

    def get_type(self):
        return self.type_token

    def add_key_token(self, key_token):
        self.key_token = key_token

    def add_value_token(self, value_token):
        self.value_token = value_token

    def get_key_token(self):
        return self.key_token
    
    def get_value_token(self):
        return self.value_token
    
    def get_arg_list(self):
        return None
    
    def get_error_token(self):
        return None

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token

# Lists, arrays, queues, and includes 
# hashsets and treesets, and set interface
class LinearType:
    def __init__(self):
        self.type_token = None
        self.value_token = None
        self.descriptor_token = None

    def add_type_token(self, type_token):
        self.type_token = type_token

    def get_type(self):
        return self.type_token

    def add_value_token(self, value_token):
        self.value_token = value_token

    def get_key_token(self):
        return None
    
    def get_value_token(self):
        return self.value_token
    
    def get_arg_list(self):
        return None
    
    def get_error_token(self):
        return None

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token

# Option, or Result
class FailableType:
    def __init__(self):
        self.type_token = None
        self.value_token = None
        self.error_token = None
        self.descriptor_token = None


    def add_type_token(self, type_token):
        self.type_token = type_token

    def get_type(self):
        return self.type_token

    def add_value_token(self, value_token):
        self.value_token = value_token

    def add_alternate_token(self, error_token):
        self.error_token = error_token

    def get_key_token(self):
        return None
    
    def get_value_token(self):
        return self.value_token
    
    def get_arg_list(self):
        return None
    
    def get_error_token(self):
        return self.error_token

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token


class FunctionType:
    def __init__(self):
        self.arg_type_list = list()
        self.return_type_token = None
        self.descriptor_token = None
        self.type_token = None

    def add_argument(self, arg_token):
        self.arg_type_list.append(arg_token)
    
    def add_return_type(self, return_type_token):
        self.return_type_token = return_type_token

    def get_key_token(self):
        return None
    
    def get_value_token(self):
        return self.return_type_token
    
    def get_arg_list(self):
        return self.arg_type_list
    
    def get_error_token(self):
        return None

    def add_descriptor_token(self, token):
        self.descriptor_token = token
        self.type_token = token

    def get_descriptor_token(self):
        return self.descriptor_token

