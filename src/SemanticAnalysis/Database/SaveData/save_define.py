from SemanticAnalysis.Database.SaveData.saver import Saver
#from SemanticAnalysis.analysis_utilities import split_path_and_file_name

def save_define(analyzer, ast_node):
    define_saver = DefineSaver(ast_node)
    analyzer.save_item_to_data_store(define_saver)

"""
Must save the following:
    FunctionType
    FailableType (option / result)
    LinearType (collections)
    KeyValueType
"""
class DefineSaver(Saver):
    def __init__(self, define_ast):
        self.define = define_ast

    def save_to_db(self, database):
        type_name_table = database.get_table("typenames")
        define_table = database.get_table("defines")

        current_module_id = database.get_current_module_id()
        # file_path = self.define.descriptor_token.filename
        # current_directory_path, current_file_name = split_path_and_file_name(file_path)

        # print(f"directory path: {current_directory_path}")
        # print(f"filename: {current_file_name}")

        object_id = database.save_object(self.import_stmt)

        new_type_name = self.define.descriptor_token

        define_table.insert(
            object_id,
            self.define.sub_type.get_descriptor_token(),
            new_type_name,
            self.define.get_key_token(),
            self.define.get_value_token(),
            self.define.get_arg_list(),
            self.define.get_error_token()
        )

        type_name_table.insert(
            new_type_name,
            "defined_type",
            current_module_id,
            object_id
        )
