from ASTComponents.ExternalComponents.import_statement import ImportStatement
from TestingComponents.testing_utilities import token_to_json
from symbols import EOF

class TestingImportStatement:
    def __init__(self):
        self.import_statement = ImportStatement()
    
    def set_as_library(self):
        self.import_statement.set_as_library()

    def set_as_module(self):
        self.import_statement.set_as_module()

    def new_path_item(self, path_node_token, direction_token):
        self.import_statement.new_path_item(path_node_token, direction_token)

    def new_import_item(self, name_token, new_name_token):
        self.import_statement.new_import_item(name_token, new_name_token)
    
    def print_literal(self, repr_list: list) -> None:
        path_string = self.import_statement.import_type + ' '
        for path_item in self.import_statement.path_list:
            path_string += path_item.node_token.literal + self.path_tok_for_lit_list(path_item.direction_token) + ' '
        for import_item in self.import_statement.import_list:
            path_string += import_item.name_token.literal + ' '
        repr_list.append(path_string.rstrip(' '))

    def print_token_types(self, type_list: list) -> None:
        path_string = self.import_statement.import_type.upper() + ' '
        for path_item in self.import_statement.path_list:
            path_string += path_item.node_token.type_symbol + self.path_tok_for_type_list(path_item.direction_token) + ' '
        for import_item in self.import_statement.import_list:
            path_string += import_item.name_token.type_symbol + ' '
        type_list.append(path_string.rstrip(' '))

    def path_tok_for_type_list(self, path_tok):
        if path_tok is None:
            return ""
        if path_tok.type_symbol == EOF:
            return ""
        return path_tok.type_symbol

    def path_tok_for_lit_list(self, path_tok):
        if path_tok is None:
            return ""
        if path_tok.type_symbol == EOF:
            return ""
        return path_tok.literal


    def to_json(self) -> dict:
        return {
            "type" : "import",
            "name" : self.path_json(),
            "import_list" : self.import_list_json(),
            "import_type" : self.import_statement.import_type
        }

    def path_json(self):
        path_list = self.import_statement.path_list
        if len(path_list) == 1:
            return {
                "node" : token_to_json(path_list[0].node_token),
                "direction" : token_to_json(path_list[0].direction_token)
            }
        path_items = list()
        for path_item in path_list:
            path_items.append({
                "node" : token_to_json(path_item.node_token),
                "direction" : token_to_json(path_item.direction_token)
            })
        return path_items
    
    def import_list_json(self):
        import_list = self.import_statement.import_list
        if len(import_list) == 1:
            item_json = {
                "name" : token_to_json(import_list[0].name_token),
                "alias" : token_to_json(import_list[0].new_name_token)
            }
            return item_json
        import_items = list()
        for import_item in import_list:
            item_json = {
                "name" : token_to_json(import_item.name_token),
                "alias" : token_to_json(import_item.new_name_token)
            }
            import_items.append(item_json)
        return import_items
