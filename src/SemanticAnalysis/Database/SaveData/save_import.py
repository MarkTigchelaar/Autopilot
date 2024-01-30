from SemanticAnalysis.Database.SaveData.saver import Saver
from SemanticAnalysis.AnalysisComponents.analysis_utilities  import split_path_and_file_name

def save_import(analyzer, ast_node):
    enum_saver = ImportSaver(ast_node)
    analyzer.save_item_to_data_store(enum_saver)

# import a from module test..path..to..module_folder.can

# Any file from inside a module can import from the same "other module".
# Collect all imports from same module in one place.
# Take filename from import item token (stop gap measure, but is pretty close, so whatever)
class ImportSaver(Saver):
    def __init__(self, import_ast):
        self.import_stmt = import_ast

    def save_to_db(self, database):
        path_item = self.import_stmt.path_list[0]
        if path_item.node_token:
            file_path = path_item.node_token.file_name
        else:
            file_path = path_item.direction_token.file_name

        _, current_file_name = split_path_and_file_name(file_path)
    

        import_table = database.get_table("imports")
        file_table = database.get_table("files")
        current_module_id = database.get_current_module_id()
        
        object_id = database.save_object(self.import_stmt)

        import_table.insert(
            object_id,
            current_module_id,
            current_file_name,
            self.import_stmt.path_list,
            self.import_stmt.import_list
        )

        if file_table.is_file_defined(object_id, current_file_name):
            raise Exception(f"INTERNAL ERROR: file {file_path} has been processed already")
        if not file_table.is_file_defined(current_module_id, current_file_name):
            file_table.insert(current_file_name, current_module_id)