from SemanticAnalysis.Database.SaveData.saver import Saver
from SemanticAnalysis.analysis_utilities import split_path_and_file_name

def save_module(analyzer, ast_node):
    enum_saver = ModuleSaver(ast_node)
    analyzer.save_item_to_data_store(enum_saver)


class ModuleSaver(Saver):
    def __init__(self, module_ast):
        self.module = module_ast

    def save_to_db(self, database):      
        module_name = self.module.name
        file_path = self.module.name.file_name
        directory_path, file_name = split_path_and_file_name(file_path)

        # Coupling? yeah, but savers know how to save!
        module_table = database.get_table("modules")
        file_table = database.get_table("files")
        type_name_table = database.get_table("typenames")

        object_id = None
        if module_table.is_module_defined(module_name.literal) and module_table.is_same_module(module_name, directory_path):
            object_id = module_table.get_module_id_by_name_and_path(module_name.literal, directory_path)
        else:
            object_id = database.save_object(self.module)
            module_table.insert(module_name, directory_path, object_id)

        if object_id is None:
            raise Exception("INTERNAL ERROR: module object id is none")

        if file_table.is_file_defined(object_id, file_name):
            raise Exception(f"INTERNAL ERROR: file {file_path} has been processed already")

        file_table.insert(file_name, object_id)

        # if type_name_table detects it is defined, get category, must be "module_name"
        if type_name_table.is_name_defined_in_table(module_name.literal, object_id):
            # This is done to avoid redefining the same module, in different source files.
            if type_name_table.get_category_by_name_and_module_id(module_name, object_id) != "module_name":
                type_name_table.insert(module_name, "module_name", object_id, object_id)
        else:
            type_name_table.insert(module_name, "module_name", object_id, object_id)
        database.set_current_module_id(object_id)
