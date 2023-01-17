from Parsing.ASTComponents.ExternalComponents.module_statement import ModuleStatement
from TestingComponents.testing_utilities import token_to_json


class TestingModuleStatement:
    def __init__(self):
        self.module_statement = ModuleStatement()

    def add_name(self, name_token):
        self.module_statement.add_name(name_token)

    def print_literal(self, repr_list: list) -> None:
        repr_list.append(self.module_statement.name.literal)


    def print_token_types(self, type_list: list) -> None:
        type_list.append(self.module_statement.name.type_symbol)
    
    def to_json(self) -> dict:
        return {
            "type" : "module",
            "name" : token_to_json(self.module_statement.name)
        }
