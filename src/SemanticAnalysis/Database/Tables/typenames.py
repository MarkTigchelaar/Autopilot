class TypeNameTable:
    def __init__(self):
        self.categories = [
            "module_name",
            "struct",
            "enum",
            "error",
            "union",
            "defined_type",
            "interface",
            "fn_header",
            # "function",
            "unittest",
        ]
        self.by_id = dict()
        self.by_name = dict()
        self.by_category = dict()
        self.by_module_id = dict()

    def get_size(self):
        count = 0
        for key in self.by_category:
            count += len(self.by_category[key])
        return count

    def has_contents(self):
        return len(self.by_name) + len(self.by_category) + len(self.by_module_id) > 0

    def insert(self, name, category, module_id, object_id):
        if category not in self.categories:
            raise Exception(f"INTERNAL ERROR: category '{category}' not recognized")
        # what about types in othermodules?

        row = TypeRow(category, module_id, object_id, name)
        if module_id not in self.by_module_id:
            self.by_module_id[module_id] = []
        self.by_module_id[module_id].append(row)

        if object_id not in self.by_id:
            self.by_id[object_id] = row

        if self.is_name_defined_in_table(name.literal, category):
            return

        if name.literal not in self.by_name:
            self.by_name[name.literal] = []
        self.by_name[name.literal].append(row)

        if category not in self.by_category:
            self.by_category[category] = []

        found = False
        for type_name in self.by_category[category]:
            if type_name.literal == name.literal:
                found = True
                break
        if not found:
            self.by_category[category].append(name)

    def is_name_defined_in_table(self, name, category):
        if name not in self.by_name:
            return False
        matched_rows = self.by_name[name]
        for row in matched_rows:
            if row.category == category:
                return True
        return False

    def is_name_defined_in_module(self, name, module_id):
        if name not in self.by_name:
            return False
        matched_rows = self.by_name[name]
        for row in matched_rows:
            if row.module_id == module_id:
                return True
        return False

    def get_categories_by_name_and_module_id(self, name, module_id):
        matched_rows = self.get_rows_by_name_and_module(name, module_id)
        categories = []
        for row in matched_rows:
            if row.module_id == module_id:
                categories.append(row.category)
        if len(categories) < 1:
            raise Exception(
                "INTERNAL ERROR: module id not found, could not retrieve category"
            )
        return categories

    def get_rows_by_name_and_module(self, name, module_id):
        if name not in self.by_name:
            raise Exception(f"INTERNAL ERROR: type '{name}' not found")
        matched_rows = self.by_name[name]
        rows = []
        for row in matched_rows:
            if row.module_id == module_id:
                rows.append(row)
        if len(rows) < 1:
            raise Exception(
                "INTERNAL ERROR: module id not found, could not retrieve category"
            )
        return rows

    def get_names_by_category(self, category_name):
        if category_name not in self.by_category:
            return []
        return self.by_category[category_name]

    def get_items_by_module_id(self, module_id):
        if module_id not in self.by_module_id:
            return []
        return self.by_module_id[module_id]

    def get_item_by_id(self, object_id):
        return self.by_id[object_id]

    def is_already_built_in_type_token(self, name, category, module_id, object_id):
        if name in self.by_name:
            items = self.by_name[name]
            for item in items:
                if item.category == category:
                    return True
        return False

    def is_object_defined(self, object_id):
        return object_id in self.by_id


class TypeRow:
    def __init__(self, category, module_id, object_id, name_token):
        self.category = category
        self.module_id = module_id
        self.object_id = object_id
        self.name_token = name_token
