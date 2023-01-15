from Parsing.ASTComponents.ExternalComponents.function_header_statement import FunctionHeaderStatement, FunctionArgument
from TestingComponents.testing_utilities import token_to_json

class TestingFunctionHeader:
    def __init__(self):
        self.function_header = FunctionHeaderStatement()

    def add_name(self, name_token):
        self.function_header.add_name(name_token)

    def add_arg(self, argument):
        self.function_header.add_arg(argument)

    def add_return_type(self, return_type_token):
        self.function_header.add_return_type(return_type_token)

    def add_acyclic_field(self, acyclic_token):
        self.function_header.add_acyclic_field(acyclic_token)

    def set_as_public(self, is_public):
        self.function_header.set_as_public(is_public)

    def print_literal(self, repr_list: list) -> None:
        if self.function_header.acyclic_token:
            repr_list.append(self.function_header.acyclic_token.literal + " ")
        if self.function_header.is_public:
            repr_list.append("pub" + " ")
        repr_list.append(self.function_header.name_token.literal + " ")
        for arg in self.function_header.arguments:
            arg.print_literal(repr_list)
        if self.function_header.return_type_token:
            repr_list.append(self.function_header.return_type_token.literal + " ")

    def print_token_types(self, type_list: list) -> None:
        if self.function_header.acyclic_token:
            type_list.append(self.function_header.acyclic_token.type_symbol + " ")
        if self.function_header.is_public:
            type_list.append("PUB" + " ")
        type_list.append(self.function_header.name_token.type_symbol + " ")
        for arg in self.function_header.arguments:
            arg.print_token_types(type_list)
        if self.function_header.return_type_token:
            type_list.append(self.function_header.return_type_token.type_symbol + " ")

    def to_json(self) -> dict:
        return {
            "type" : "function_header",
            "name" : token_to_json(self.function_header.name_token),
            "arguments" : self.items_json_list(),
            "return_type" : token_to_json(self.function_header.return_type_token),
            "header_attributes" : {
                "acyclic" : token_to_json(self.function_header.acyclic_token),
                "public" : self.function_header.is_public
            }
        }

    def items_json_list(self) -> list:
        item_list = list()
        for fn_arg in self.function_header.arguments:
            item_list.append(fn_arg.to_json())
        return item_list

class TestingFunctionArgument:
    def __init__(self):
        self.function_argument = FunctionArgument()

    def add_name(self, arg_name_token):
        self.function_argument.add_name(arg_name_token)

    def add_type(self, arg_type_token):
        self.function_argument.add_type(arg_type_token)

    def add_default_value(self, default_value_token):
        self.function_argument.add_default_value(default_value_token)

    def print_literal(self, repr_list: list) -> None:
        repr_list.append(self.function_argument.arg_name_token.literal + " ")
        repr_list.append(self.function_argument.arg_type_token.literal + " ")
        if self.function_argument.default_value_token:
            repr_list.append(self.function_argument.default_value_token.literal + " ")

    def print_token_types(self, type_list: list) -> None:
        type_list.append(self.function_argument.arg_name_token.type_symbol + " ")
        type_list.append(self.function_argument.arg_type_token.type_symbol + " ")
        if self.function_argument.default_value_token:
            type_list.append(self.function_argument.default_value_token.type_symbol + " ")

    def to_json(self) -> dict:
        return {
            "name" : token_to_json(self.function_argument.arg_name_token),
            "type" : token_to_json(self.function_argument.arg_type_token),
            "default" : token_to_json(self.function_argument.default_value_token)
        }
