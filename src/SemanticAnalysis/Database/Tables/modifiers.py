class ModifierTable:
    def __init__(self):
        self.by_id = dict()

    def get_size(self):
        return len(self.by_id)

    def has_contents(self):
        return len(self.by_id) > 0

    def insert(self, object_id, modifier_list):
        if object_id in self.by_id:
            raise Exception("INTERNAL ERROR: id of modifed ast node already defined")

        self.by_id[object_id] = modifier_list

    def is_object_defined(self, object_id):
        return object_id in self.by_id

    def get_modifier_list_by_id(self, object_id):
        return self.by_id[object_id]
