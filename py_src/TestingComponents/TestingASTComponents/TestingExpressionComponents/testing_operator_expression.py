from Parsing.ASTComponents.ExpressionComponents.operator_expression import OperatorExpression
from TestingComponents.testing_utilities import token_to_json

class TestingOperatorExpression:
    def __init__(self):
        self.exp = OperatorExpression()

    def add_name(self, operator_token):
        self.exp.add_name(operator_token)

    def add_lhs_exp(self, lhs_exp):
        self.exp.add_lhs_exp(lhs_exp)
    
    def add_rhs_exp(self, rhs_exp):
        self.exp.add_rhs_exp(rhs_exp)

    def print_literal(self, repr_list:list) -> None:
        repr_list.append("(")
        self.exp.left_expression.print_literal(repr_list)
        repr_list.append(' ' + self.exp.operator_token.literal + ' ')
        self.exp.right_expression.print_literal(repr_list)
        repr_list.append(")")

    def print_token_types(self, type_list: list) -> None:
        type_list.append("(")
        self.exp.left_expression.print_token_types(type_list)
        type_list.append(' ' + self.exp.operator_token.type_symbol + ' ')
        self.exp.right_expression.print_token_types(type_list)
        type_list.append(")")

    def to_json(self) -> dict:
        return {
            "type" : "binary",
            "token" : token_to_json(self.exp.operator_token),
            "lhs_exp" : self.exp.left_expression.to_json(),
            "rhs_exp" : self.exp.right_expression.to_json()
        }