class Database:
    def __init__(self, error_manager):
        self.objects = []
        self.error_manager = error_manager
        self.tables = {
            "typenames": TypeNameTable(),
            "modules": ModuleTable(),
            "files": FileTable(),
            "imports": ImportTable(),
            "defines": DefineTable(),
            "enumerables": EnumerableTable(),
            "modifiers": ModifierTable(),
            "functions": FunctionTable(),
            "fn_headers": FunctionHeaderTable(),
            "interfaces": InterfaceTable(),
            "statements": StatementTable(),
            "structs": StructTable(),
        }
        self.current_module_id = None

    def set_current_module_id(self, module_id):
        self.current_module_id = module_id

    def get_current_module_id(self):
        return self.current_module_id
    
    def get_tablename_for_object(self, object_id):
        for table_name in self.tables:
            table = self.get_table(table_name)
            if table_name in ("typenames"):
                continue
            if table.is_object_defined(object_id):
                return table_name
        raise Exception("INTERNAL ERROR: table name for object id was not found")

    def save_object(self, object_ref):
        self.objects.append(object_ref)
        return len(self.objects) - 1
    
    def get_object(self, object_id):
        return self.objects[object_id]

    def get_table(self, table_name):
        if table_name not in self.tables:
            raise Exception(
                f'INTERNAL ERROR: database asked for table "{table_name}", but isn\'t present'
            )
        return self.tables[table_name]

    def object_count(self):
        return len(self.objects)


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
            #"function",
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
        #what about types in othermodules?

        row = TypeRow(category, module_id, object_id, name)
        if module_id not in self.by_module_id:
            self.by_module_id[module_id] = []
        self.by_module_id[module_id].append(row)


        if object_id not in self.by_id:
            self.by_id[object_id] = row

        if self.is_name_defined_in_table(
            name.literal, category
        ):
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


class ModuleTable:
    def __init__(self):
        self.by_name = dict()
        self.by_path = dict()
        self.by_id = dict()

    def has_contents(self):
        return len(self.by_name) + len(self.by_path) + len(self.by_id) > 0

    def get_size(self):
        return len(self.by_id)

    def insert(self, module_name, path, id):
        if module_name.literal not in self.by_name:
            self.by_name[module_name.literal] = []
        self.by_name[module_name.literal].append(ModulePathIdRow(path, id, module_name))

        if path not in self.by_path:
            self.by_path[path] = []
        self.by_path[path].append(ModuleNameIdRow(module_name, id))

        if id not in self.by_id:
            self.by_id[id] = ModuleNamePathRow(module_name, path)
        else:
            raise Exception("INTERNAL ERROR: module id already defined")

    def is_object_defined(self, module_id):
        return module_id in self.by_id

    def is_module_defined(self, module_name):
        return module_name in self.by_name

    def is_same_module(self, module_name, path):
        return self.get_module_id_by_name_and_path(module_name.literal, path) != None

    def get_module_id_by_name_and_path(self, module_name, path):
        mods = self.get_modules_data_for_name(module_name)
        for mod in mods:
            if mod.path == path:
                return mod.module_id
        return None

    def get_modules_data_for_name(self, module_name):
        if module_name not in self.by_name:
            raise Exception("INTERNAL ERROR: module name not found")
        return self.by_name[module_name]

    def get_module_for_id(self, id):
        if id not in self.by_id:
            raise Exception("INTERNAL ERROR: module id not found")
        return self.by_id[id]


class ModulePathIdRow:
    def __init__(self, path, module_id, name):
        self.path = path
        self.module_id = module_id
        self.name = name


class ModuleNameIdRow:
    def __init__(self, module_name, id):
        self.module_name = module_name
        self.id = id


class ModuleNamePathRow:
    def __init__(self, module_name, path):
        self.module_name = module_name
        self.path = path


class FileTable:
    def __init__(self):
        self.by_name = dict()
        self.by_module_id = dict()

    def get_size(self):
        count = 0
        for key in self.by_module_id:
            count += len(self.by_module_id[key])
        return count

    def has_contents(self):
        return len(self.by_name) + len(self.by_module_id) > 0

    def insert(self, file_name, module_id):
        if self.is_file_defined(module_id, file_name):
            raise Exception("INTERNAL ERROR: File is already defined.")

        if file_name not in self.by_name:
            self.by_name[file_name] = []
        self.by_name[file_name].append(module_id)

        if module_id not in self.by_module_id:
            self.by_module_id[module_id] = set()
        self.by_module_id[module_id].add(file_name)

    def is_file_defined(self, module_id, file_name):
        files_in_module = self.get_module_file_names(module_id)
        for file in files_in_module:
            if file == file_name:
                return True
        return False

    def get_module_file_names(self, module_id):
        if module_id not in self.by_module_id:
            return []
        return self.by_module_id[module_id]

    def get_module_ids_by_file_name(self, file_name):
        if file_name not in self.by_name:
            raise Exception("INTERNAL ERROR: filename not found")
        return self.by_name[file_name]
    
    def is_object_defined(self, _):
        return False














class ImportTableRow:
    def __init__(self, object_id, current_module_id, filename, path, items, imported_module_name, imported_module_name_token):
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

        row = ImportTableRow(object_id, current_module_id, filename, path, items, imported_module_name, imported_module_name_token)
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
            object_id
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
        object_id
    ):
        self.built_in_type_token = built_in_type_token
        self.new_type_name_token = new_type_name_token
        self.key_type = key_type
        self.value_type = value_type
        self.arg_list = arg_list
        self.result_type = result_type
        self.current_module_id = current_module_id
        self.object_id = object_id


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


class InterfaceTable:
    def __init__(self):
        self.by_id = dict()
        self.by_module_id = dict()

    def get_size(self):
        return len(self.by_id)

    def has_contents(self):
        return len(self.by_id) > 0

    def insert(self, object_id, module_id, fn_header_ids):
        if object_id in self.by_id:
            raise Exception("INTERNAL ERROR: id of modifed ast node already defined")

        self.by_id[object_id] = fn_header_ids

        if module_id not in self.by_module_id:
            self.by_module_id[module_id] = []
        self.by_module_id[module_id].append(object_id)

    def is_object_defined(self, object_id):
        return object_id in self.by_id

    def get_item_by_id(self, id):
        row = self.by_id[id]
        return row

    def get_rows_by_module_id(self, module_id):
        if module_id not in self.by_module_id:
            raise Exception("INTERNAL ERROR: Module Id not found")
        return self.by_module_id[module_id]


class FunctionTable:
    def __init__(self):
        self.by_id = dict()
        self.by_module_id = dict()

    def get_size(self):
        return len(self.by_id)

    def has_contents(self):
        return len(self.by_id) > 0

    def insert(self, object_id, header_id, module_id):
        if object_id in self.by_id:
            raise Exception("INTERNAL ERROR: id of modifed ast node already defined")
        row = FunctionTableRow(object_id, header_id)
        self.by_id[object_id] = row

        if module_id not in self.by_module_id:
            self.by_module_id[module_id] = []
        self.by_module_id[module_id].append(row)

    def is_object_defined(self, object_id):
        return object_id in self.by_id

    def get_item_by_id(self, object_id):
        return self.by_id[object_id]


class FunctionTableRow:
    def __init__(self, object_id, header_id):
        self.object_id = object_id
        self.header_id = header_id


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


class StatementTable:
    def __init__(self):
        self.by_key = dict()
        self.by_container_id = dict()

    def get_size(self):
        return len(self.by_key)

    def has_contents(self):
        return len(self.by_key) > 0

    def insert(
        self, stmt_type_token, statement, container_object_id, sequence_num, scope_depth
    ):
        if stmt_type_token is None:
            print(type(statement))
        # Container id is always the function, or unittest object id.
        potential_key = StatementTableKey(sequence_num, container_object_id)
        if potential_key in self.by_key:
            raise Exception("INTERNAL ERROR: id of modifed ast node already defined")

        row = StatementRow(
            stmt_type_token, statement, container_object_id, sequence_num, scope_depth
        )
        self.by_key[potential_key] = row

        if container_object_id not in self.by_container_id:
            self.by_container_id[container_object_id] = list()
        self.by_container_id[container_object_id].append(row)

    def is_object_defined(self, container_object_id, sequence_num):
        potential_key = StatementTableKey(sequence_num, container_object_id)
        return potential_key in self.by_key

    def get_item_by_id_and_seq_num(self, container_object_id, sequence_num):
        return self.by_key[StatementTableKey(sequence_num, container_object_id)]

    def get_rows_by_container_id(self, container_id):
        rows = self.by_container_id[container_id]
        rows.sort(key=lambda x: x.sequence_num, reverse=False)
        return rows


class StatementTableKey:
    def __init__(self, sequence, container_id):
        self.sequence = sequence
        self.container_id = container_id

    def __hash__(self):
        return int(str(self.sequence) + str(self.container_id))

    def __eq__(self, other):
        return (
            self.sequence == other.sequence and self.container_id == other.container_id
        )


class StatementRow:
    def __init__(
        self,
        stmt_type_token,
        statement,
        container_object_id,  # function / unittest
        sequence_num,  # ordering of statements, depth first
        scope_depth,
    ):
        self.statement = statement
        self.container_object_id = container_object_id
        self.sequence_num = sequence_num
        self.scope_depth = scope_depth
        self.stmt_type_token = stmt_type_token


class StructTable:
    def __init__(self):
        self.by_id = dict()
        self.by_module_id = dict()

    def get_size(self):
        return len(self.by_id)

    def has_contents(self):
        return len(self.by_id) > 0

    def insert(self, name_token, interfaces, fields, object_id, module_id, function_ids, functions):
        if object_id in self.by_id:
            raise Exception("INTERNAL ERROR: id of modifed ast node already defined")
        row = StructTableRow(name_token, object_id, interfaces, fields, function_ids, functions)
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
    def __init__(self, name_token, object_id, interfaces, fields, function_ids, functions):
        self.name_token = name_token
        self.object_id = object_id
        self.interfaces = interfaces
        self.fields = fields
        self.function_ids = function_ids
        self.functions = functions
