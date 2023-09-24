from SemanticAnalysis.Database.SaveData.saver import Saver
from SemanticAnalysis.analysis_utilities import split_path_and_file_name

def save_enum(analyzer, ast_node):
    enum_saver = EnumSaver(ast_node)
    analyzer.save_item_to_data_store(enum_saver)


class EnumSaver(Saver):
    def __init__(self, enum_ast):
        self.enum = enum_ast

    def save_to_db(self, database):
        name = self.enum.name
        items = self.enum.item_list
        contained_type = self.enum.general_type
        public_token = self.enum.public_token

        current_module_id = database.get_current_module_id()
        object_id = database.save_object(self.enum)
        type_name_table = database.get_table("typenames")
        enumerable_table = database.get_table("enumerables")
        modifier_table = database.get_table("modifiers")
        file_table = database.get_table("files")
        #module_table = database.get_table("modules")

        file_path = name.file_name
        # dir path not needed, refers to the current module, which knows its dir path.
        _, file_name = split_path_and_file_name(file_path)

        type_name_table.insert(
            name,
            "enum",
            current_module_id,
            object_id
        )
        enumerable_table.insert(
            object_id,
            items,
            contained_type
        )
        modifier_table.insert(
            object_id,
            [public_token]
        )
        if file_table.is_file_defined(object_id, file_name):
            raise Exception(f"INTERNAL ERROR: file {file_path} has been processed already")
        if not file_table.is_file_defined(current_module_id, file_name):
            file_table.insert(file_name, current_module_id)
