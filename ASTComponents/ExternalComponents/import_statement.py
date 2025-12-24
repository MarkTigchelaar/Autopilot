class ImportStatement:
    def __init__(self):
        self.import_type = None
        self.source_name = None #Token
        self.path_list = list()
        self.import_list = list()

    def set_as_library(self):
        self.import_type = "library"
    
    def is_library(self):
        return self.import_type == "library"

    def set_as_module(self):
        self.import_type = "module"

    def set_source_name(self, name):
        self.source_name = name

    def get_source_name(self):
        return self.source_name

    def new_path_item(self, path_node_token, direction_token):
        path_node = PathItem(path_node_token, direction_token)
        self.path_list.append(path_node)

    def get_import_list(self):
        return self.import_list

    def get_path_list(self):
        return self.path_list
    
    def get_imported_name_token(self):
        return self.source_name

    def new_import_item(self, name_token, new_name_token):
        self.import_list.append(ImportItem(name_token, new_name_token))

class ImportItem:
    def __init__(self, name_token, new_name_token):
        self.name_token = name_token
        self.new_name_token = new_name_token
        self.actual_item_ref = None

    def get_visible_item_name(self):
        if self.new_name_token is not None:
            return self.new_name_token
        return self.get_actual_item_name()
    
    def get_actual_item_name(self):
        if not self.name_token:
            raise Exception("INTERNAL ERROR: import item has no name")
        return self.name_token
    
    def set_ref_to_actual_type(self, actual_item):
        self.actual_item_ref = actual_item
    
    def get_ref_to_actual_item(self):
        return self.actual_item_ref 


class PathItem:
    def __init__(self, node_token, direction_token):
        self.node_token = node_token
        self.direction_token = direction_token
