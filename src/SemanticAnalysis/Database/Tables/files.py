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
