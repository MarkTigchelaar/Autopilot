from Parsing.ASTComponents.ExternalComponents.union_statement import UnionStatement
from TestingComponents.testing_utilities import token_to_json

class TestingUnionStatement:
    def __init__(self):
        self.union_statement = UnionStatement()

    def add_name(self, name):
        self.union_statement.add_name(name)

    def add_item(self, item_name_token, type_token):
        self.union_statement.add_item(item_name_token, type_token)

    def print_literal(self, repr_list: list) -> None:
        union_string = self.union_statement.name_token.literal
        for item in self.union_statement.items:
            union_string += self.print_list_item(item)
        repr_list.append(union_string.rstrip(' '))

    def print_list_item(self, item):
        name = ' ' + item.item_name_token.literal + ' '
        type = item.type_token.literal
        return name + type
    
    def print_token_types(self, type_list: list) -> None:
        union_type = self.union_statement.name_token.type_symbol
        type_list.append(union_type)
        for item in self.union_statement.items:
            type_list.append(' ' + item.item_name_token.type_symbol + ' ')
            type_list.append(item.type_token.type_symbol)

    def to_json(self) -> dict:
        return {
            "type" : "union",
            "name" : token_to_json(self.union_statement.name_token),
            "items" : self.items_json_list()
        }

    def items_json_list(self):
        item_list = list()
        for item in self.union_statement.items:
            item_list.append(self.item_to_json(item))
        return item_list

    def item_to_json(self, item):
        return {
            "name" : token_to_json(item.item_name_token),
            "item_type" : token_to_json(item.type_token)
        }
