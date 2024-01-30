from SemanticAnalysis.Database.SaveData.saver import Saver
from SemanticAnalysis.Database.SaveData.save_function import FunctionSaver
from SemanticAnalysis.analysis_utilities import split_path_and_file_name

def save_struct(analyzer, ast_node):
    struct_saver = StructSaver(ast_node)
    analyzer.save_item_to_data_store(struct_saver)


class StructSaver(Saver):
    def __init__(self, struct_ast):
        self.struct = struct_ast

    def save_to_db(self, database):
        current_module_id = database.get_current_module_id()
        type_name_table = database.get_table("typenames")
        struct_table = database.get_table("structs")
        file_table = database.get_table("files")
        modifier_table = database.get_table("modifiers")

        file_path = self.struct.name_token.file_name
        _, file_name = split_path_and_file_name(file_path)

        object_id = database.save_object(self.struct)
        
        function_ids = list()
        for fn in self.struct.functions:
            function_saver = FunctionSaver(fn)
            function_saver.save_to_db(database)
            function_id = function_saver.object_id
            function_ids.append(function_id)

        type_name_table.insert(
            self.struct.name_token,
            "struct",
            current_module_id,
            object_id
        )

        struct_table.insert(
            self.struct.name_token,
            self.struct.interfaces,
            self.struct.fields,
            object_id,
            current_module_id,
            function_ids,
            self.struct.functions
        )

        acyclic_token = self.struct.acyclic_token
        inline_token = self.struct.inline_token
        public_token = self.struct.public_token
        mods = []
        for tok in [acyclic_token, inline_token, public_token]:
            if tok:
                mods.append(tok)
        modifier_table.insert(
            object_id,
            mods
        )

        if file_table.is_file_defined(object_id, file_name):
            raise Exception(f"INTERNAL ERROR: file {file_path} has been processed already")
        if not file_table.is_file_defined(current_module_id, file_name):
            file_table.insert(file_name, current_module_id)
