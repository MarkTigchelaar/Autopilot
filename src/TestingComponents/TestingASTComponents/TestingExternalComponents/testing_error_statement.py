from ASTComponents.ExternalComponents.error_statement import ErrorStatement
from TestingComponents.testing_utilities import token_to_json


class TestingErrorStatement:
    def __init__(self):
        self.error_statement = ErrorStatement()

    def add_name(self, name_token):
        self.error_statement.add_name(name_token)

    def new_item(self, item_name):
        self.error_statement.new_item(item_name)

    def add_public_token(self, public_token):
        self.error_statement.add_public_token(public_token)

    def print_literal(self, repr_list: list) -> None:
        error_string = self.error_statement.name_token.literal + ' '
        for item in self.error_statement.items:
            error_string += item.literal + ' '
        repr_list.append(error_string.rstrip(' '))


    def print_token_types(self, type_list: list) -> None:
        error_type = self.error_statement.name_token.type_symbol + ' '
        type_list.append(error_type)
        for item in self.error_statement.items:
            type_list.append(item.type_symbol + ' ')


    def to_json(self) -> dict:
        return {
            "type" : "error",
            "name" : token_to_json(self.error_statement.name_token),
            "error_list" : self.make_error_list()
        }


    def make_error_list(self):
        errors = list()
        for item in self.error_statement.items:
            errors.append(token_to_json(item))
        return errors
