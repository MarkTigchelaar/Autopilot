class EnumerableTable:
    def __init__(self):
        self.by_id = dict()

    def get_size(self):
        return len(self.by_id)

    def has_contents(self):
        return len(self.by_id) > 0

    def insert(self, object_id, item_list, general_type_token=None):
        if object_id in self.by_id:
            raise Exception(
                "INTERNAL ERROR: id of enumerable statement already defined"
            )

        new_row = EnumerableTableRow(item_list, general_type_token)
        self.by_id[object_id] = new_row

    def is_object_defined(self, object_id):
        return object_id in self.by_id

    def get_general_type_token_by_id(self, id):
        row = self.by_id[id]
        return row.general_type_token

    def get_items_by_id(self, id):
        row = self.by_id[id]
        return row.item_list

    def get_item_by_id(self, id):
        row = self.by_id[id]
        return row


class EnumerableTableRow:
    def __init__(self, item_list, general_type_token):
        self.item_list = item_list
        self.general_type_token = general_type_token
