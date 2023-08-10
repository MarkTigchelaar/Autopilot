from SemanticAnalysis.Database.SaveData.saver import Saver
from SemanticAnalysis.analysis_utilities import split_path_and_file_name

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
        #pass
        # collect all imports from same module (files are in same module)
        
        # This is a bit of a hack, but all tokens do keep this data
        path_item = self.import_stmt.path_list[0]
        file_path = path_item.node_token.filename

        current_directory_path, current_file_name = split_path_and_file_name(file_path)
        
        print(f"directory path: {current_directory_path}")
        print(f"filename: {current_file_name}")

        import_table = database.get_table("imports")
        file_table = database.get_table("files")
        current_module_id = database.get_current_module_id()
        # Since no comparisons of one import item list to another is needed,
        # don't unpack import list into rows
        # if file_table.is_file_defined(current_module_id, current_file_name):
        #     raise Exception(f"INTERNAL ERROR: file {file_path} has been processed already")
        
        object_id = database.save_object(self.import_stmt)
        file_table.insert(current_file_name, current_module_id)

        import_table.insert(
            object_id,
            current_module_id,
            current_file_name,
            self.import_stmt.path_list,
            self.import_stmt.import_list
        )
