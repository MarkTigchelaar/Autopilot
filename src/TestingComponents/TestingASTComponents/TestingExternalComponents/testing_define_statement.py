from Parsing.ASTComponents.ExternalComponents.define_statement import \
DefineStatement, KeyValueType, LinearType, FailableType, FunctionType
from TestingComponents.testing_utilities import token_to_json



class TestingDefineStatement:
    def __init__(self):
        self.define_statement = DefineStatement()

    def add_subtype(self, sub_type):
        self.define_statement.add_subtype(sub_type)

    def add_definition(self, definition_token):
        self.define_statement.add_definition(definition_token)

    def print_literal(self, repr_list: list) -> None:
        self.define_statement.sub_type.print_literal(repr_list)
        repr_list.append('-> ' + self.define_statement.new_type_name_token.literal)

    def print_token_types(self, type_list: list) -> None:
        self.define_statement.sub_type.print_token_types(type_list)
        type_list.append('-> ' + self.define_statement.new_type_name_token.type_symbol)

    def to_json(self) -> dict:
        return {
            "type" : "define",
            "definition" : self.define_statement.sub_type.to_json(),
            "new_name" : token_to_json(self.define_statement.new_type_name_token)
        }

# hashMaps, Dictionarys, Map interface
class TestingKeyValueType:
    def __init__(self):
        self.key_value_type = KeyValueType()

    def add_type_token(self, type_token):
        self.key_value_type.add_type_token(type_token)

    def add_key_token(self, key_token):
        self.key_value_type.add_key_token(key_token)

    def add_value_token(self, value_token):
        self.key_value_type.add_value_token(value_token)

    def print_literal(self, repr_list: list) -> None:
        repr_list.append(self.key_value_type.type_token.literal)
        repr_list.append('(' + self.key_value_type.key_token.literal + ':')
        repr_list.append(self.key_value_type.value_token.literal + ') ')

    def print_token_types(self, type_list: list) -> None:
        type_list.append(self.key_value_type.type_token.type_symbol + ' ')
        type_list.append(self.key_value_type.key_token.type_symbol + ' ')
        type_list.append(self.key_value_type.value_token.type_symbol + ' ')

    def to_json(self) -> dict:
        return {
            "map_collection_type" : token_to_json(self.key_value_type.type_token),
            "key" : token_to_json(self.key_value_type.key_token),
            "value" : token_to_json(self.key_value_type.value_token)
        }


# Lists, arrays, queues, and includes 
# hashsets and treesets, and set interface
class TestingLinearType:
    def __init__(self):
        self.linear_type = LinearType()

    def add_type_token(self, type_token):
        self.linear_type.add_type_token(type_token)

    def add_value_token(self, value_token):
        self.linear_type.add_value_token(value_token)

    def print_literal(self, repr_list: list) -> None:
        repr_list.append(self.linear_type.type_token.literal)
        repr_list.append('(' + self.linear_type.value_token.literal + ') ')

    def print_token_types(self, type_list: list) -> None:
        type_list.append(self.linear_type.type_token.type_symbol + ' ')
        type_list.append(self.linear_type.value_token.type_symbol + ' ')

    def to_json(self) -> dict:
        return {
            "linear_collection_type" : token_to_json(self.linear_type.type_token),
            "value_type" : token_to_json(self.linear_type.value_token)
        }


# Option, or Result
class TestingFailableType:
    def __init__(self):
        self.failable_type = FailableType()
    
    def add_type_token(self, type_token):
        self.failable_type.add_type_token(type_token)

    def add_value_token(self, value_token):
        self.failable_type.add_value_token(value_token)

    def add_alternate_token(self, error_token):
        self.failable_type.add_alternate_token(error_token)

    def print_literal(self, repr_list: list) -> None:
        repr_list.append(self.failable_type.type_token.literal)
        repr_list.append('(' + self.failable_type.value_token.literal)
        if self.failable_type.error_token is not None:
            repr_list.append(',' + self.failable_type.error_token.literal + ') ')
        else:
            repr_list.append(') ')
    def print_token_types(self, type_list: list) -> None:
        type_list.append(self.failable_type.type_token.type_symbol)
        type_list.append(' ' + self.failable_type.value_token.type_symbol + ' ')
        if self.failable_type.error_token is not None:
            type_list.append(self.failable_type.error_token.type_symbol + ' ')

    def to_json(self) -> dict:
        return {
            "type" : token_to_json(self.failable_type.type_token),
            "value" : token_to_json(self.failable_type.value_token),
            "alt_value" : token_to_json(self.failable_type.error_token)
        }


# moot, but could have procedure in future??
class TestingFunctionType:
    def __init__(self):
        self.function_type = FunctionType()
    
    def add_argument(self, arg_token):
        self.function_type.add_argument(arg_token)
    
    def add_return_type(self, return_type_token):
        self.function_type.add_return_type(return_type_token)

    def print_literal(self, repr_list: list) -> None:
        repr_list.append("fun(")
        repr_list.extend(','.join([arg.literal  for arg in self.function_type.arg_type_list]))
        if self.function_type.return_type_token is not None:
            repr_list.append(')' + self.function_type.return_type_token.literal + ' ')
        else:
            repr_list.append(') ')

    def print_token_types(self, type_list: list) -> None:
        type_list.append("FUN ")
        type_list.extend(' '.join([arg.type_symbol for arg in self.function_type.arg_type_list]))
        if self.function_type.return_type_token is not None:
            type_list.append(' ' + self.function_type.return_type_token.type_symbol + ' ')
        else:
            type_list.append(') ')

    def to_json(self) -> dict:
        return {
            "type" : "function_signature",
            "args" : [token_to_json(arg) for arg in self.function_type.arg_type_list],
            "return_type" : token_to_json(self.function_type.return_type_token)
        }
