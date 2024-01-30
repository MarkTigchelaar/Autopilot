from ASTComponents.ExpressionComponents.method_call_or_field_expression import MethodCallOrFieldExpression
from TestingComponents.testing_utilities import token_to_json

class TestingMethodCallOrFieldExpression:
    def __init__(self):
        self.exp = MethodCallOrFieldExpression()

    def add_lhs_exp(self, left_exp):
        self.exp.add_lhs_exp(left_exp)

    def add_field_or_methods(self, field_or_method_list):
        self.exp.add_field_or_methods(field_or_method_list)

    def print_literal(self, repr_list: list) -> None:
        self.exp.struct_name_exp.print_literal(repr_list)
        repr_list.append(".")
        i = 0
        l = len(self.exp.argument_list)
        for arg in self.exp.argument_list:
            # arg might be a field (identifier)
            # or a method (identifier with more args)
            arg.print_literal(repr_list)
            if i < l - 1:
                repr_list.append(",")
            i += 1

    def print_token_types(self, type_list: list) -> None:
        self.exp.struct_name_exp.print_token_types(type_list)
        type_list.append(" DOT ")
        i = 0
        l = len(self.exp.argument_list)
        for arg in self.exp.argument_list:
            arg.print_token_types(type_list)
            if i < l - 1:
                type_list.append(",")
            i += 1

    def to_json(self) -> dict:
        return {
            "type" : "method_call",
            "struct" : self.exp.struct_name_exp.to_json(),
            "methods" : self.args_to_json()
        }

    def args_to_json(self) -> list:
        args_json = list()
        for arg in self.exp.argument_list:
            args_json.append(arg.to_json())
        return args_json
