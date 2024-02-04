class InterfaceTable:
    def __init__(self):
        self.by_id = dict()
        self.by_module_id = dict()

    def get_size(self):
        return len(self.by_id)

    def has_contents(self):
        return len(self.by_id) > 0

    def insert(self, object_id, module_id, name, fn_header_ids):
        if object_id in self.by_id:
            raise Exception("INTERNAL ERROR: id of modifed ast node already defined")

        row = InterfaceRow(object_id, module_id, name, fn_header_ids)
        self.by_id[object_id] = row

        if module_id not in self.by_module_id:
            self.by_module_id[module_id] = []
        self.by_module_id[module_id].append(row)

    def is_object_defined(self, object_id):
        return object_id in self.by_id

    def get_item_by_id(self, id):
        row = self.by_id[id]
        return row

    def get_rows_by_module_id(self, module_id):
        if module_id not in self.by_module_id:
            raise Exception("INTERNAL ERROR: Module Id not found")
        return self.by_module_id[module_id]


class InterfaceRow:
    def __init__(self, object_id, module_id, name, fn_header_ids):
        self.object_id = object_id
        self.module_id = module_id
        self.name_token = name
        self.fn_header_ids = fn_header_ids

    def to_string(self):
        return f"InterfaceRow: object_id: {self.object_id}, module_id: {self.module_id}, name: {self.name_token}, fn_header_ids: {self.fn_header_ids}"
