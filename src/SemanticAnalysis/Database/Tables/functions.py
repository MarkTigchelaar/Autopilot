class FunctionTable:
    def __init__(self):
        self.by_id = dict()
        self.by_module_id = dict()

    def get_size(self):
        return len(self.by_id)

    def has_contents(self):
        return len(self.by_id) > 0

    def insert(self, object_id, header_id, module_id, struct_id=None):
        if object_id in self.by_id:
            raise Exception("INTERNAL ERROR: id of modifed ast node already defined")
        row = FunctionTableRow(object_id, header_id, struct_id)
        self.by_id[object_id] = row

        if module_id not in self.by_module_id:
            self.by_module_id[module_id] = []
        self.by_module_id[module_id].append(row)

    def is_object_defined(self, object_id):
        return object_id in self.by_id

    def get_item_by_id(self, object_id):
        return self.by_id[object_id]


class FunctionTableRow:
    def __init__(self, object_id, header_id, struct_id=None):
        self.object_id = object_id
        self.header_id = header_id
        self.struct_id = struct_id


class FunctionHeaderTable:
    def __init__(self):
        self.by_id = dict()

    def get_size(self):
        return len(self.by_id)

    def has_contents(self):
        return len(self.by_id) > 0

    def insert(self, object_id, header_object):
        if object_id in self.by_id:
            raise Exception("INTERNAL ERROR: id of modifed ast node already defined")

        self.by_id[object_id] = header_object

    def is_object_defined(self, object_id):
        return object_id in self.by_id

    def get_item_by_id(self, object_id):
        return self.by_id[object_id]
