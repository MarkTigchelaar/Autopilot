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
