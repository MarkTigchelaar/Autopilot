from SemanticAnalysis.Database.SaveData.saver import Saver
from SemanticAnalysis.AnalysisComponents.analysis_utilities  import split_path_and_file_name


def save_union(analyzer, ast_node):
    enum_saver = UnionSaver(ast_node)
    analyzer.save_item_to_data_store(enum_saver)


class UnionSaver(Saver):
    def __init__(self, union_ast):
        self.union = union_ast

    def save_to_db(self, database):
        name = self.union.name_token
        items = self.union.items
        public_token = self.union.public_token

        current_module_id = database.get_current_module_id()
        object_id = database.save_object(self.union)
        type_name_table = database.get_table("typenames")
        enumerable_table = database.get_table("enumerables")
        modifier_table = database.get_table("modifiers")
        file_table = database.get_table("files")

        file_path = name.file_name
        # dir path not needed, refers to the current module, which knows its dir path.
        _, file_name = split_path_and_file_name(file_path)

        type_name_table.insert(name, "union", current_module_id, object_id)
        enumerable_table.insert(object_id, items)
        mods = []
        if public_token:
            mods.append(public_token)
        modifier_table.insert(object_id, mods)

        if file_table.is_file_defined(object_id, file_name):
            raise Exception(
                f"INTERNAL ERROR: file {file_path} has been processed already"
            )
        if not file_table.is_file_defined(current_module_id, file_name):
            file_table.insert(file_name, current_module_id)
