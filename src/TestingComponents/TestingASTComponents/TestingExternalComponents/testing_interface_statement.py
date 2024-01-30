from ASTComponents.ExternalComponents.interface_statement import InterfaceStatement
from TestingComponents.testing_utilities import token_to_json


class TestingInterfaceStatement:
    def __init__(self):
        self.interface_statement = InterfaceStatement()

    def add_name(self, name_token):
        self.interface_statement.add_name(name_token)

    def add_function_headers(self, fn_headers):
        self.interface_statement.add_function_headers(fn_headers)

    def add_acyclic_token(self, acyclic_token):
        self.interface_statement.add_acyclic_token(acyclic_token)

    def add_public_token(self, public_token):
        self.interface_statement.add_public_token(public_token)

    def print_literal(self, repr_list: list) -> None:
        repr_list.append(self.interface_statement.name_token.literal + " ")
        for fn_header in self.interface_statement.fn_headers:
            fn_header.print_literal(repr_list)

    def print_token_types(self, type_list: list) -> None:
        type_list.append(self.interface_statement.name_token.type_symbol + " ")
        for fn_header in self.interface_statement.fn_headers:
            fn_header.print_token_types(type_list)

    def to_json(self) -> dict:
        return {
            "type" : "interface",
            "name" : token_to_json(self.interface_statement.name_token),
            "function_headers" : self.items_json_list(),
            "attributes" : {
                "acyclic" : token_to_json(self.interface_statement.acyclic_token),
                "public" : token_to_json(self.interface_statement.public_token)
            }
        }

    def items_json_list(self) -> list:
        item_list = list()
        for fn_header in self.interface_statement.fn_headers:
            item_list.append(fn_header.to_json())
        return item_list
