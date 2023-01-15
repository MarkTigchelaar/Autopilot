from Parsing.ASTComponents.ExternalComponents.unittest_statement import UnittestStatement
from TestingComponents.testing_utilities import token_to_json


class TestingUnittestStatement:
    def __init__(self):
        self.unittest_statement = UnittestStatement()

    def add_test_name(self, name_token):
        self.unittest_statement.add_test_name(name_token)

    def add_statements(self, statements):
        self.unittest_statement.add_statements(statements)

    def print_literal(self, repr_list: list) -> None:
        if self.unittest_statement.name:
            repr_list.append(self.unittest_statement.name.literal)
        

    def print_token_types(self, type_list: list) -> None:
        if self.unittest_statement.name:
            type_list.append(self.unittest_statement.name.type_symbol)

    def to_json(self) -> dict:
        return {
            "type" : "unittest",
            "name" : token_to_json(self.unittest_statement.name),
            "statements" : self.items_json_list()
        }

    def items_json_list(self) -> list:
        item_list = list()
        for stmt in self.unittest_statement.statements:
            item_list.append(stmt.to_json())
        return item_list
