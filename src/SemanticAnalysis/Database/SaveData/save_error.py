from SemanticAnalysis.Database.SaveData.saver import Saver
from SemanticAnalysis.AnalysisComponents.analysis_utilities  import split_path_and_file_name

def save_error(analyzer, ast_node):
    enum_saver = ErrorSaver(ast_node)
    analyzer.save_item_to_data_store(enum_saver)


class ErrorSaver(Saver):
    def __init__(self, error_ast):
        self.error = error_ast

    def save_to_db(self, database):
        name = self.error.name_token
        items = self.error.items
        public_token = self.error.public_token

        current_module_id = database.get_current_module_id()
        object_id = database.save_object(self.error)
        type_name_table = database.get_table("typenames")
        enumerable_table = database.get_table("enumerables")
        modifier_table = database.get_table("modifiers")
        file_table = database.get_table("files")

        file_path = name.file_name
        # dir path not needed, refers to the current module, which knows its dir path.
        _, file_name = split_path_and_file_name(file_path)
        items = [ErrorListItem(item) for item in items]
        type_name_table.insert(
            name,
            "error",
            current_module_id,
            object_id
        )
        enumerable_table.insert(
            object_id,
            items,
            None
        )
        mods = []
        if public_token:
            mods.append(public_token)
        modifier_table.insert(
            object_id,
            mods
        )
        if file_table.is_file_defined(object_id, file_name):
            raise Exception(f"INTERNAL ERROR: file {file_path} has been processed already")
        if not file_table.is_file_defined(current_module_id, file_name):
            file_table.insert(file_name, current_module_id)

# This is 100% a shoehorn for Errors
# Should have made each error entry like this, not just enums
class ErrorListItem:
    def __init__(self, item_name_token, default_value_token = None):
        self.item_name_token = item_name_token
        self.default_value_token = default_value_token

    def get_value(self):
        return self.default_value_token