class ImportTableRow:
    def __init__(
        self,
        object_id,
        current_module_id,
        filename,
        path,
        items,
        imported_module_name,
        imported_module_name_token,
    ):
        self.id = object_id
        self.current_module_id = current_module_id
        self.filename = filename
        self.path = path
        self.items = items
        self.imported_module_name = imported_module_name
        self.imported_module_name_token = imported_module_name_token


class ImportTable:
    def __init__(self):
        self.by_current_module_id = dict()
        self.by_id = dict()
        self.by_file_name = dict()
        self.by_imported_module_name = dict()

    def get_size(self):
        return len(self.by_id)

    def has_contents(self):
        temp = len(self.by_current_module_id) + len(self.by_id)
        temp += len(self.by_file_name) + len(self.by_imported_module_name)
        return temp > 0

    def insert(self, object_id, current_module_id, filename, path, items):
        if object_id in self.by_id:
            raise Exception("INTERNAL ERROR: id of import already defined")
        if current_module_id not in self.by_current_module_id:
            self.by_current_module_id[current_module_id] = []
        if filename not in self.by_file_name:
            self.by_file_name[filename] = []

        imported_module_name = path[-1].node_token.literal
        imported_module_name_token = path[-1].node_token
        if imported_module_name not in self.by_imported_module_name:
            self.by_imported_module_name[imported_module_name] = []

        row = ImportTableRow(
            object_id,
            current_module_id,
            filename,
            path,
            items,
            imported_module_name,
            imported_module_name_token,
        )
        self.by_id[object_id] = row
        self.by_current_module_id[current_module_id].append(row)
        self.by_file_name[filename].append(row)
        self.by_imported_module_name[imported_module_name].append(row)

    def is_object_defined(self, object_id):
        return object_id in self.by_id

    def get_items_by_id(self, object_id):
        row = self.by_id[object_id]
        return row.items

    def get_row_by_id(self, object_id):
        return self.by_id[object_id]

    def get_path_by_id(self, object_id):
        row = self.by_id[object_id]
        return row.path

    def get_module_data_by_module_name(self, module_name):
        if module_name in self.by_imported_module_name:
            return self.by_imported_module_name[module_name]
        return None

    def module_has_imports(self, module_id):
        return module_id in self.by_current_module_id

    def get_imports_by_module_id(self, module_id):
        return self.by_current_module_id[module_id]
