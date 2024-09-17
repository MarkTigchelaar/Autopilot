

class ImportStatement:
    def __init__(self):
        self.import_type = None
        self.path_list = list()
        self.import_list = list()

    def set_as_library(self):
        self.import_type = "library"

    def set_as_module(self):
        self.import_type = "module"

    def new_path_item(self, path_node_token, direction_token):
        path_node = PathItem(path_node_token, direction_token)
        self.path_list.append(path_node)

    def get_import_list(self):
        return self.import_list

    def get_path_list(self):
        return self.path_list
    
    def get_imported_name_token(self):
        return self.get_path_list()[-1].node_token

    def new_import_item(self, name_token, new_name_token):
        self.import_list.append(ImportItem(name_token, new_name_token))

class ImportItem:
    def __init__(self, name_token, new_name_token):
        self.name_token = name_token
        self.new_name_token = new_name_token


class PathItem:
    def __init__(self, node_token, direction_token):
        self.node_token = node_token
        self.direction_token = direction_token
