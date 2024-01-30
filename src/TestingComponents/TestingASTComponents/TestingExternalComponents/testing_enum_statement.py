from ASTComponents.ExternalComponents.enum_statement import EnumStatement
from TestingComponents.testing_utilities import token_to_json

class TestingEnumStatement:
    def __init__(self):
        self.enum_statement = EnumStatement()
    
    def add_name(self, name):
        self.enum_statement.add_name(name)

    def new_item(self, item_name_token, default_value_token) -> None:
        self.enum_statement.new_item(item_name_token, default_value_token)

    def add_public_token(self, public_token):
        self.enum_statement.add_public_token(public_token)

    def add_general_type(self, type_token) -> None:
        self.enum_statement.add_general_type(type_token)

    def print_literal(self, repr_list: list) -> None:
        enum_name = self.enum_statement.name
        if enum_name is None:
            enum_name = "null"
        else:
            enum_name = enum_name.literal
        enum_type = self.enum_statement.general_type
        if enum_type is None:
            enum_type = "null"
        else:
            enum_type = enum_type.literal
        enum_string = "("
        enum_string += "name : " + enum_name + ", "
        enum_string += "type : " + enum_type + ", "
        enum_string += "items : ["
        for item in self.enum_statement.item_list:
            enum_string += self.print_list_item(item) + ", "
        enum_string = enum_string.rstrip(", ")
        enum_string += "])"
        repr_list.append(enum_string)

    def print_list_item(self, item) -> str:
        item_name = item.item_name_token.literal
        default_value = "null"
        if item.default_value_token is not None:
            default_value = item.default_value_token.literal
        item_string = "(name : " + item_name + ", "
        item_string += "default_value : " + default_value + ")"
        return item_string

    def print_token_types(self, type_list: list) -> None:
        type_list.append(self.enum_statement.name.type_symbol + ' ')
        enum_type = self.enum_statement.general_type
        if enum_type is not None:
            type_list.append(enum_type.type_symbol + ' ')
        for item in self.enum_statement.item_list:
            type_list.append(item.item_name_token.type_symbol + ' ')
            if item.default_value_token is not None:
                type_list.append(item.default_value_token.type_symbol + ' ')
            else:
                type_list.append("NULL ")

    def to_json(self) -> dict:
        return {
            "type" : "enum",
            "name" : token_to_json(self.enum_statement.name),
            "fields" : self.items_json_list(),
            "enum_type" : token_to_json(self.enum_statement.general_type)
        }

    def items_json_list(self) -> list:
        item_list = list()
        for item in self.enum_statement.item_list:
            item_list.append(self.item_to_json(item))
        return item_list

    def item_to_json(self, item):
        return {
            "name" : token_to_json(item.item_name_token),
            "default_value" : token_to_json(item.default_value_token)
        }
