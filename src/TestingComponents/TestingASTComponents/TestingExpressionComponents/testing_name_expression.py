from ASTComponents.ExpressionComponents.name_expression import NameExpression
from TestingComponents.testing_utilities import token_to_json


class TestingNameExpression:
    def __init__(self):
        self.exp = NameExpression()
    
    def add_name(self, name_token):
        self.exp.add_name(name_token)
    
    def print_literal(self, repr_list: list) -> None:
        repr_list.append(self.exp.token.literal)

    def print_token_types(self, type_list: list) -> None:
        type_list.append(self.exp.token.type_symbol)

    def to_json(self) -> dict:
        return {
            "type" : "identifier_or_literal",
            "token" : token_to_json(self.exp.token)
        }
