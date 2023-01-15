from Parsing.ASTComponents.InternalComponents.break_statement import BreakStatement
from TestingComponents.testing_utilities import token_to_json


class TestingBreakStatement:
    def __init__(self):
        self.break_statement = BreakStatement()

    def add_label_name(self, label_name):
        self.break_statement.add_label_name(label_name)

    def print_literal(self, repr_list: list) -> None:
        repr_list.append(self.break_statement.label_name_token.literal)

    def print_token_types(self, type_list: list) -> None:
        type_list.append(self.break_statement.label_name_token.type_symbol)

    def to_json(self) -> dict:
        return {
            "type" : "break",
            "destination" : token_to_json(self.break_statement.label_name_token)
        }
