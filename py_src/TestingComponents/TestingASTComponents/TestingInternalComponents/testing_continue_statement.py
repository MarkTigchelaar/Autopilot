from Parsing.ASTComponents.InternalComponents.continue_statement import ContinueStatement
from TestingComponents.testing_utilities import token_to_json


class TestingContinueStatement:
    def __init__(self):
        self.continue_statement = ContinueStatement()

    def add_descriptor_token(self, continue_token):
        self.continue_statement.add_descriptor_token(continue_token)

    def print_literal(self, repr_list: list) -> None:
        repr_list.append(self.continue_statement.continue_token.literal)

    def print_token_types(self, type_list: list) -> None:
        type_list.append(self.continue_statement.continue_token.type_symbol)

    def to_json(self) -> dict:
        return {
            "type" : "continue"
        }
