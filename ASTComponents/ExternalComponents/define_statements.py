# HashMaps, Dictionarys, Map interface
class KeyValueType:
    def __init__(self):
        self.type_variant_token = None
        self.key_token = None
        self.value_token = None
        self.new_name_token = None
        self.key_type_ref = None
        self.value_type_ref = None

    def set_key_type_ref(self, type_ref):
        self.key_type_ref = type_ref

    def set_value_type_ref(self, type_ref):
        self.value_type_ref = type_ref

    def all_items_have_types(self) -> bool:
        return (self.key_type_ref is not None) and (self.value_type_ref is not None)

    def add_type_variant_token(self, type_variant_token):
        self.type_variant_token = type_variant_token

    def get_type_variant_token(self):
        return self.type_variant_token

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

    def add_new_name_token(self, token):
        self.new_name_token = token

    def get_new_name_token(self):
        return self.new_name_token

    def is_public(self):
        return False

    def get_name(self):
        return self.new_name_token


class HashType:
    def __init__(self):
        self.type_variant_token = None
        self.value_token = None
        self.new_name_token = None
        self.key_type_ref = None

    def set_key_type_ref(self, type_ref):
        self.key_type_ref = type_ref

    def all_items_have_types(self) -> bool:
        return self.key_type_ref is not None

    def add_type_variant_token(self, type_variant_token):
        self.type_variant_token = type_variant_token

    def get_type_variant_token(self):
        return self.type_variant_token

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

    def add_new_name_token(self, token):
        self.new_name_token = token

    def get_new_name_token(self):
        return self.new_name_token

    def is_public(self):
        return False

    def get_name(self):
        return self.new_name_token


# Lists, arrays, queues, and includes
# hashsets and treesets, and set interface
class ListType:
    def __init__(self):
        self.type_variant_token = None
        self.value_token = None
        self.new_name_token = None
        self.value_type_ref = None

    def set_value_type_ref(self, type_ref):
        self.value_type_ref = type_ref

    def all_items_have_types(self) -> bool:
        return self.value_type_ref is not None

    def add_type_variant_token(self, type_variant_token):
        self.type_variant_token = type_variant_token

    def get_type_variant_token(self):
        return self.type_variant_token

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

    def add_new_name_token(self, token):
        self.new_name_token = token

    def get_new_name_token(self):
        return self.new_name_token

    def is_public(self):
        return False

    def get_name(self):
        return self.new_name_token


class QueueType:
    def __init__(self):
        self.type_variant_token = None
        self.value_token = None
        self.new_name_token = None
        self.value_type_ref = None

    def set_value_type_ref(self, type_ref):
        self.value_type_ref = type_ref

    def all_items_have_types(self) -> bool:
        return self.value_type_ref is not None

    def add_type_variant_token(self, type_variant_token):
        self.type_variant_token = type_variant_token

    def get_type_variant_token(self):
        return self.type_variant_token

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

    def add_new_name_token(self, token):
        self.new_name_token = token

    def get_new_name_token(self):
        return self.new_name_token

    def is_public(self):
        return False

    def get_name(self):
        return self.new_name_token


class StackType:
    def __init__(self):
        self.type_variant_token = None
        self.value_token = None
        self.new_name_token = None
        self.value_type_ref = None

    def set_value_type_ref(self, type_ref):
        self.value_type_ref = type_ref

    def all_items_have_types(self) -> bool:
        return self.value_type_ref is not None

    def add_type_variant_token(self, type_variant_token):
        self.type_variant_token = type_variant_token

    def get_type_variant_token(self):
        return self.type_variant_token

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

    def add_new_name_token(self, token):
        self.new_name_token = token

    def get_new_name_token(self):
        return self.new_name_token

    def is_public(self):
        return False

    def get_name(self):
        return self.new_name_token


# Option, or Result
class OptionType:
    def __init__(self):
        self.type_variant_token = None
        self.value_token = None
        self.error_token = None
        self.new_name_token = None
        self.value_type_ref = None
        self.null_instance_type = None

    def set_value_type_ref(self, type_ref):
        self.value_type_ref = type_ref

    def all_items_have_types(self) -> bool:
        return self.value_type_ref is not None
    
    def set_null_type(self, null_instance_type) -> None:
        self.null_instance_type = null_instance_type

    def add_type_variant_token(self, type_variant_token):
        self.type_variant_token = type_variant_token

    def get_type_variant_token(self):
        return self.type_variant_token

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

    def add_new_name_token(self, token):
        self.new_name_token = token

    def get_new_name_token(self):
        return self.new_name_token
    
    def get_name(self):
        return self.new_name_token

    def is_public(self):
        return False


class ResultType:
    def __init__(self):
        self.type_variant_token = None
        self.value_token = None
        self.error_token = None
        self.new_name_token = None
        self.error_type_ref = None
        self.value_type_ref = None

    def set_error_type_ref(self, type_ref):
        self.error_type_ref = type_ref

    def set_value_type_ref(self, type_ref):
        self.value_type_ref = type_ref

    def all_items_have_types(self) -> bool:
        return (self.error_type_ref is not None) and (self.value_type_ref is not None)

    def add_type_variant_token(self, type_variant_token):
        self.type_variant_token = type_variant_token

    def get_type_variant_token(self):
        return self.type_variant_token

    def add_value_token(self, value_token):
        self.value_token = value_token

    def get_value_token(self):
        return self.value_token
    
    def get_error_token(self):
        return self.error_token

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

    def add_new_name_token(self, token):
        self.new_name_token = token

    def get_new_name_token(self):
        return self.new_name_token

    def is_public(self):
        return False

    def get_name(self):
        return self.new_name_token


class FunctionType:
    def __init__(self):
        self.arg_type_list = list()
        self.return_type_token = None
        self.new_name_token = None
        self.type_variant_token = None
        self.return_type_ref = None
        self.arg_type_ref_list = None

    def set_return_type_ref(self, type_ref):
        self.return_type_ref = type_ref

    def set_arg_types_ref(self, arg_type_ref_list):
        self.arg_type_ref_list = arg_type_ref_list

    def all_items_have_types(self) -> bool:
        if not self.return_type_ref is not None:
            return False
        if len(self.arg_type_ref_list) != len(self.arg_type_list):
            return False
        for i in range(len(self.arg_type_ref_list)):
            if (
                self.arg_type_list[i].get_name().literal
                != self.arg_type_ref_list[i].get_name().literal
            ):
                return False
        return True

    def add_argument(self, arg_token):
        self.arg_type_list.append(arg_token)

    def add_return_type(self, return_type_token):
        self.return_type_token = return_type_token

    def get_return_type(self):
        return self.return_type_token

    def get_key_token(self):
        return None

    def get_value_token(self):
        return self.return_type_token

    def get_arg_list(self):
        return self.arg_type_list

    def get_error_token(self):
        return None

    def add_new_name_token(self, token):
        self.new_name_token = token
        # self.type_variant_token = token

    def get_new_name_token(self):
        return self.new_name_token

    def is_public(self):
        return False

    def get_name(self):
        return self.new_name_token

    def add_type_variant_token(self, token):
        self.type_variant_token = token

    def get_type_variant_token(self):
        return self.type_variant_token
