from ASTComponents.ExpressionComponents.collection_access_expression import CollectionAccessExpression


class TestingCollectionAccessExpression:
    def __init__(self):
        self.exp = CollectionAccessExpression()

    def add_name_exp(self, name_exp):
        self.exp.add_name_exp(name_exp)

    def add_argument_list(self, argument_list):
        self.exp.add_argument_list(argument_list)

    def print_literal(self, repr_list: list) -> None:
        self.exp.collection_name_exp.print_literal(repr_list)
        repr_list.append("[")
        i = 0
        l = len(self.exp.argument_list)
        for arg in self.exp.argument_list:
            arg.print_literal(repr_list)
            if i < l - 1:
                repr_list.append(",")
            i += 1
        repr_list.append("]")

    def print_token_types(self, type_list: list) -> None:
        self.exp.collection_name_exp.print_token_types(type_list)
        type_list.append("[")
        i = 0
        l = len(self.exp.argument_list)
        for arg in self.exp.argument_list:
            arg.print_token_types(type_list)
            if i < l - 1:
                type_list.append(",")
            i += 1
        type_list.append("]")

    def to_json(self) -> dict:
        return {
            "type" : "collection_access",
            "collection_name" : self.exp.collection_name_exp.to_json(),
            "arguments" : self.args_to_json()
        }

    def args_to_json(self) -> list:
        args_json = list()
        for arg in self.exp.argument_list:
            args_json.append(arg.to_json())
        return args_json