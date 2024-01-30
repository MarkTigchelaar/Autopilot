class StructTable:
    def __init__(self):
        self.by_id = dict()
        self.by_module_id = dict()

    def get_size(self):
        return len(self.by_id)

    def has_contents(self):
        return len(self.by_id) > 0

    def insert(
        self,
        name_token,
        interfaces,
        fields,
        object_id,
        module_id,
        function_ids,
        functions,
    ):
        if object_id in self.by_id:
            raise Exception("INTERNAL ERROR: id of modifed ast node already defined")
        row = StructTableRow(
            name_token, object_id, interfaces, fields, function_ids, functions
        )
        self.by_id[object_id] = row

        if module_id not in self.by_module_id:
            self.by_module_id[module_id] = list()
        self.by_module_id[module_id].append(row)

    def is_object_defined(self, object_id):
        return object_id in self.by_id

    def get_item_by_id(self, object_id):
        return self.by_id[object_id]

    def is_module_id_defined(self, module_id):
        return module_id in self.by_module_id

    def get_items_by_module_id(self, module_id):
        if module_id not in self.by_module_id:
            raise Exception("INTERNAL ERROR: module id not found")
        return self.by_module_id[module_id]


class StructTableRow:
    def __init__(
        self, name_token, object_id, interfaces, fields, function_ids, functions
    ):
        self.name_token = name_token
        self.object_id = object_id
        self.interfaces = interfaces
        self.fields = fields
        self.function_ids = function_ids
        self.functions = functions
