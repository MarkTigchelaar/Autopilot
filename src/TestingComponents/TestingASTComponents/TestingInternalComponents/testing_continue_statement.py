from Parsing.ASTComponents.InternalComponents.continue_statement import ContinueStatement
from TestingComponents.testing_utilities import token_to_json


class TestingContinueStatement:
    def __init__(self):
        self.continue_statement = ContinueStatement()

    def print_literal(self, repr_list: list) -> None:
        repr_list.append(self.continue_statement.get_descriptor_token().literal)

    def print_token_types(self, type_list: list) -> None:
        type_list.append(self.continue_statement.get_descriptor_token().type_symbol)

    def to_json(self) -> dict:
        return {
            "type" : "continue"
        }

    def add_descriptor_token(self, token):
        self.continue_statement.add_descriptor_token(token)

    def get_descriptor_token(self):
        return self.continue_statement.get_descriptor_token()