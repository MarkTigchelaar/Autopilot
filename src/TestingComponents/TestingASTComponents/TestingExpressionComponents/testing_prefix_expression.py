from ASTComponents.ExpressionComponents.prefix_expression import PrefixExpression
from TestingComponents.testing_utilities import token_to_json


class TestingPrefixExpression:
    def __init__(self):
        self.exp = PrefixExpression()

    def add_name(self, token):
        self.exp.add_name(token)
    
    def add_rhs_exp(self, rhs_expression):
        self.exp.add_rhs_exp(rhs_expression)

    def print_literal(self, repr_list: list) -> None:
        repr_list.append("(")
        repr_list.append(self.exp.token.literal)
        self.exp.rhs_exp.print_literal(repr_list)
        repr_list.append(")")

    def print_token_types(self, type_list: list) -> None:
        type_list.append("(")
        type_list.append(self.exp.token.type_symbol + ' ')
        self.exp.rhs_exp.print_token_types(type_list)
        type_list.append(")")

    def to_json(self) -> dict:
        return {
            "type" : "prefix",
            "token" : token_to_json(self.exp.token),
            "rhs_exp" : self.exp.rhs_exp.to_json()
        }