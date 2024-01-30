class UnittestTable:
    def __init__(self):
        self.by_id = dict()
        self.by_module_id = dict()

    def get_size(self):
        return len(self.by_id)

    def has_contents(self):
        return len(self.by_id) > 0

    def insert(self, object_id, module_id, name):
        if object_id in self.by_id:
            raise Exception("INTERNAL ERROR: id of modifed ast node already defined")
        row = UnittestTableRow(object_id, module_id, name)
        self.by_id[object_id] = row

        if module_id not in self.by_module_id:
            self.by_module_id[module_id] = []
        self.by_module_id[module_id].append(row)


class UnittestTableRow:
    def __init__(self, object_id, module_id, name):
        self.object_id = object_id
        self.module_id = module_id
        self.name = name
