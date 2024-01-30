from ASTComponents.ExpressionComponents.collection_expression import CollectionExpression
from Parsing.parsing_utilities import get_collection_literal

class TestingCollectionExpression:
    def __init__(self):
        self.exp = CollectionExpression()

    def add_lhs_type(self, lhs_type):
        self.exp.add_lhs_type(lhs_type)
    
    def add_expression(self, expression_array):
        self.exp.add_expression(expression_array)
    
    def add_rhs_type(self, rhs_type):
        self.exp.add_rhs_type(rhs_type)

    def print_literal(self, repr_list: list) -> None:
        repr_list.append(get_collection_literal(self.exp.left_type))
        i = 0
        l = len(self.exp.expression_array)
        for arg in self.exp.expression_array:
            arg.print_literal(repr_list)
            if i < l - 1:
                repr_list.append(",")
            i += 1
        repr_list.append(get_collection_literal(self.exp.rhs_type))

    def print_token_types(self, type_list: list) -> None:
        type_list.append(get_collection_literal(self.exp.left_type))
        i = 0
        l = len(self.exp.expression_array)
        for arg in self.exp.expression_array:
            arg.print_token_types(type_list)
            if i < l - 1:
                type_list.append(",")
            i += 1
        type_list.append(get_collection_literal(self.exp.rhs_type))

    def to_json(self) -> dict:
        return {
            "type" : "collection",
            "left_delimiter" : self.exp.left_type,
            "elements" : self.elements_to_json(),
            "right_delimiter" : self.exp.rhs_type
        }

    def elements_to_json(self)-> list:
        args_json = list()
        for arg in self.exp.expression_array:
            args_json.append(arg.to_json())
        return args_json
