



# After parsing is done, as well as local analysis, a list of these objects
# is what is produced. This is the raw data that is then used to generate
# the IL for autopilot, called APIL.
class RawModule:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.directory_path = None
        self.included_files = []
        self.excluded_files = []
        self.module_statements = []
        # self.defines = []
        self.key_value_defines = []
        self.linear_type_defines = []
        self.failable_type_defines = []
        self.function_type_defines = []
        self.enums = []
        self.errors = []
        self.interfaces = []
        self.unions = []
        self.structs = []
        self.functions = []
        self.imports = []
        self.unit_tests = []
        self.built_in_libs = dict()

    def get_module_name_token(self):
        return self.module_statements[0].get_name()
    
    def get_built_in_libs(self):
        return self.built_in_libs

    def item_count(self):
        count = len(self.module_statements)
        count += len(self.key_value_defines)
        count += len(self.linear_type_defines)
        count += len(self.failable_type_defines)
        count += len(self.function_type_defines)
        count += len(self.enums)
        count += len(self.errors)
        count += len(self.interfaces)
        count += len(self.unions)
        count += len(self.structs)
        count += len(self.functions)
        count += len(self.imports)
        count += len(self.unit_tests)
        return count
    

    def get_module_item_name_tokens(self):
        items = self.get_all_non_import_items()
        return [item.get_name() for item in items]



    def get_all_non_import_items(self):
        items = []
        items.extend([item for item in self.key_value_defines])
        items.extend([item for item in self.linear_type_defines])
        items.extend([item for item in self.failable_type_defines])
        items.extend([item for item in self.function_type_defines])
        items.extend([item for item in self.enums])
        items.extend([item for item in self.errors])
        items.extend([item for item in self.unions])
        items.extend([item for item in self.structs])
        items.extend([item for item in self.functions])
        items.extend([item for item in self.unit_tests])
        return items




class RawModuleCollection:
    def __init__(self, raw_modules, error_manager):
        self.raw_modules = raw_modules
        self.error_manager = error_manager
        self.built_in_libs = dict()

    def get_error_manager(self):
        return self.error_manager

    def has_errors(self):
        return self.error_manager.has_errors(True)
    
    def report_errors(self):
        self.error_manager.report_errors()
        
    def get_raw_modules(self):
        return self.raw_modules

    def add_built_in_libs(self, built_in_libs):
        self.built_in_libs.update(built_in_libs)
        for module in self.raw_modules:
            module.built_in_libs.update(built_in_libs)
    
    def get_built_in_libs(self):
        return self.built_in_libs