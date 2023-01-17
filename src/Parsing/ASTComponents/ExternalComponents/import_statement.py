

class ImportStatement:
    def __init__(self):
        self.import_type = None
        self.path_list = list()
        self.import_list = list()

    def set_as_library(self):
        self.import_type = "library"

    def set_as_module(self):
        self.import_type = "module"

    def new_path_item(self, path_item_token):
        self.path_list.append(path_item_token)

    def new_import_item(self, name_token, new_name_token):
        self.import_list.append(ImportItem(name_token, new_name_token))

class ImportItem:
    def __init__(self, name_token, new_name_token):
        self.name_token = name_token
        self.new_name_token = new_name_token