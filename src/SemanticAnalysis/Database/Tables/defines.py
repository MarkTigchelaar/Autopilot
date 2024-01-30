class DefineTable:
    def __init__(self):
        self.by_id = dict()
        self.by_module_id = dict()
        self.by_user_defined_type_token = dict()

    def get_size(self):
        return len(self.by_id)

    def has_contents(self):
        return len(self.by_id) + len(self.by_user_defined_type_token) > 0

    def insert(
        self,
        current_module_id,
        object_id,
        built_in_type_token,
        new_type_name_token,
        key_type,
        value_type,
        arg_list,
        result_type,
    ):
        if object_id in self.by_id:
            raise Exception("INTERNAL ERROR: id of define statement already defined")

        if new_type_name_token.literal not in self.by_user_defined_type_token:
            self.by_user_defined_type_token[new_type_name_token.literal] = []
        new_row = DefineTableRow(
            built_in_type_token,
            new_type_name_token,
            key_type,
            value_type,
            arg_list,
            result_type,
            current_module_id,
            object_id,
        )
        self.by_id[object_id] = new_row
        if current_module_id not in self.by_module_id:
            self.by_module_id[current_module_id] = list()
        self.by_module_id[current_module_id].append(new_row)
        self.by_user_defined_type_token[new_type_name_token.literal].append(new_row)

    def is_object_defined(self, object_id):
        return object_id in self.by_id

    def get_item_by_id(self, object_id):
        return self.by_id[object_id]

    def is_module_id_defined(self, module_id):
        return module_id in self.by_module_id

    def get_items_by_module_id(self, module_id):
        return self.by_module_id[module_id]


class DefineTableRow:
    def __init__(
        self,
        built_in_type_token,
        new_type_name_token,
        key_type,
        value_type,
        arg_list,
        result_type,
        current_module_id,
        object_id,
    ):
        self.built_in_type_token = built_in_type_token
        self.new_type_name_token = new_type_name_token
        self.key_type = key_type
        self.value_type = value_type
        self.arg_list = arg_list
        self.result_type = result_type
        self.current_module_id = current_module_id
        self.object_id = object_id
