#from SemanticAnalysis.Database.table import Table
#from SemanticAnalysis.Database.table_makers import make_all_tables

class Database:
    def __init__(self, error_manager):
        #self.tables = make_all_tables()
        self.objects = []
        #self.modules = ModuleTable()
        self.error_manager = error_manager
        self.tables = {
            "typenames": TypeNameTable(),
            "modules" : ModuleTable(),
            "files" : FileTable(),
            "imports" : ImportTable(),
            "defines" : DefineTable(),
            "enumerables" : EnumerableTable(),
            "modifiers" : ModifierTable()
        }
        self.current_module_id = None
    
    def set_current_module_id(self, module_id):
        self.current_module_id = module_id

    def get_current_module_id(self):
        return self.current_module_id

    def process_queries(self, analyzer):
        pass # begin analysis
        # for i, ast_object in enumerate(self.objects):
            # for key in self.tables:
                # if i in self.tables[key]:
                    #analyzer.analyze_object(ast_object, key, self)

    def save_object(self, object_ref):
        self.objects.append(object_ref)
        return len(self.objects) - 1


    def get_table(self, table_name):
        if table_name not in self.tables:
            raise Exception(f"INTERNAL ERROR: database asked for table \"{table_name}\", but isn't present")
        return self.tables[table_name]
    
    def object_count(self):
        return len(self.objects)


    
    # def next_type_id(self):
    #     temp = self.type_id_sequence
    #     self.type_id_sequence += 1
    #     return temp

    # def make_blank_row(self, table_name):
    #     if table_name not in self.tables:
    #         raise Exception("INTERNAL ERROR: table name not found")
    #     return self.tables[table_name].make_blank_row()
    


# Tables:
# class Table:
#     def __init__(self, error_manager):
#         self.error_manager = error_manager



class TypeNameTable:
    def __init__(self):
        self.categories = [
            "module_name",
            "import_item",
            "struct",
            "enum",
            "error",
            "union",
            "defined_type"
        ]
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

        if self.is_name_defined_in_table(name, category):#, module_id, object_id):
            return

        if name.literal not in self.by_name:
            self.by_name[name.literal] = []
        self.by_name[name.literal].append(TypeRow(category, module_id, object_id))
        
        
        if category not in self.by_category:
            self.by_category[category] = []

        found = False
        for type_name in self.by_category[category]:
            if type_name.literal == name.literal:
                found = True
                break
        if not found:
            self.by_category[category].append(name)

        if module_id not in self.by_module_id:
            self.by_module_id[module_id] = []
        self.by_module_id[module_id].append(name)

    def is_name_defined_in_table(self, name, category):
        if name not in self.by_name:
            return False
        matched_rows = self.by_name[name]
        for row in matched_rows:
            if row.category == category:
                return True
        return False
    
    def get_category_by_name_and_module_id(self, name, module_id):
        if name not in self.by_name:
            raise Exception(f"INTERNAL ERROR: type '{name}' not found")
        matched_rows = self.by_name[name]
        for row in matched_rows:
            if row.module_id == module_id:
                return row.category
        raise Exception("INTERNAL ERROR: module id not found, could not retrieve category")

    def get_names_by_category(self, category_name):
        if category_name not in self.by_category:
            return []
        return self.by_category[category_name]
    
    def get_names_by_module_id(self, module_id):
        if module_id not in self.by_module_id:
            return []
        return self.by_module_id[module_id]
    
    def is_already_defined_type(self, name, category, module_id, object_id):
        if name in self.by_name:
            items = self.by_name[name]
            for item in items:
                if item.category == category:
                    return True
        return False
        
class TypeRow:
    def __init__(self, category, module_id, object_id):
        self.category = category
        self.module_id = module_id
        self.object_id = object_id





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
        self.by_name[module_name.literal].append(ModulePathIdRow(path, id))

        if path not in self.by_path:
            self.by_path[path] = []
        self.by_path[path].append(ModuleNameIdRow(module_name, id))

        if id not in self.by_id:
            self.by_id[id] = ModuleNamePathRow(module_name, path)
        else:
            raise Exception("INTERNAL ERROR: module id already defined")
        #self.by_id[id].append(ModuleNamePathRow(module_name, path))
    
    def is_module_defined(self, module_name):
        return module_name in self.by_name
    
    def is_same_module(self, module_name, path):
        return self.get_module_id_by_name_and_path(module_name.literal, path) != None

    def get_module_id_by_name_and_path(self, module_name, path):
        mods = self.get_modules_data_for_name(module_name)
        for mod in mods:
            if mod.path == path:
                return mod.id
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
    def __init__(self, path, id):
        self.path = path
        self.id = id
    
class ModuleNameIdRow:
    def __init__(self, module_name, path):
        self.module_name = module_name
        self.path = path

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
            #raise Exception("INTERNAL ERROR: module id not found")
            return []
        return self.by_module_id[module_id]

    def get_module_ids_by_file_name(self, file_name):
        if file_name not in self.by_name:
            raise Exception("INTERNAL ERROR: filename not found")
        return self.by_name[file_name]
    


class ImportTableRow:
    def __init__(self, object_id, current_module_id, filename, path, items):
        self.id = object_id
        self.current_module_id = current_module_id
        self.filenames = [filename]
        self.path = path
        self.items = items




class ImportTable:
    def __init__(self):
        self.by_current_module_id = dict()
        self.by_id = dict()
        self.by_file_name = dict()
        self.by_imported_module_name = dict()

    def get_size(self):
        return 0

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
        if imported_module_name not in self.self.by_imported_module_name:
            self.by_imported_module_name[imported_module_name] = []

        row = ImportTableRow(object_id, current_module_id, filename, path, items)
        self.by_id[object_id] = row
        self.by_current_module_id[current_module_id].append(row)
        self.by_file_name[filename].append(row)
        self.by_imported_module_name[imported_module_name].append(row)



class DefineTable:
    def __init__(self):
        self.by_id = dict()
        self.by_new_type_name = dict()

    def get_size(self):
        return 0

    def has_contents(self):
        return len(self.by_id) + len(self.by_new_type_name) > 0

    def insert(self, object_id, defined_type, new_type_name, key_type, value_type, arg_list, union_type):
        if object_id in self.by_id:
            raise Exception("INTERNAL ERROR: id of define statement already defined")

        if new_type_name.literal not in self.by_new_type_name:
            self.by_new_type_name[new_type_name.literal] = []
        new_row = DefineTableRow(
            defined_type,
            new_type_name,
            key_type,
            value_type,
            arg_list,
            union_type
        )
        self.by_id[object_id] = new_row
        self.by_new_type_name[new_type_name.literal].append(new_row)


class DefineTableRow:
        def __init__(self, defined_type, new_type_name, key_type, value_type, arg_list, error_type):
            self.defined_type = defined_type
            self.new_type_name = new_type_name
            self.key_type = key_type
            self.value_type = value_type
            self.arg_list = arg_list
            self.error_type = error_type




class EnumerableTable:
    def __init__(self):
        self.by_id = dict()

    def get_size(self):
        return len(self.by_id)

    def has_contents(self):
        return len(self.by_id) > 0

    def insert(self, object_id, item_list, general_type_token = None):
        if object_id in self.by_id:
            raise Exception("INTERNAL ERROR: id of enumerable statement already defined")

        new_row = EnumerableTableRow(
            item_list,
            general_type_token
        )
        self.by_id[object_id] = new_row
    
    def is_object_defined(self, object_id):
        return object_id in self.by_id
    
    def get_general_type_token_by_id(self, id):
        row = self.by_id[id]
        return row.general_type_token

    def get_items_by_id(self, id):
        row = self.by_id[id]
        return row.item_list


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


    


