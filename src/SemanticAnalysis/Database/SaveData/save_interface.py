from SemanticAnalysis.Database.SaveData.saver import Saver
from SemanticAnalysis.Database.SaveData.save_fn_header import FnHeaderSaver
from SemanticAnalysis.AnalysisComponents.analysis_utilities  import split_path_and_file_name

def save_interface(analyzer, ast_node):
    interface_saver = InterfaceSaver(ast_node)
    analyzer.save_item_to_data_store(interface_saver)


class InterfaceSaver(Saver):
    def __init__(self, interface_ast):
        self.interface = interface_ast

    def save_to_db(self, database):
        current_module_id = database.get_current_module_id()
        type_name_table = database.get_table("typenames")
        interface_table = database.get_table("interfaces")
        modifier_table = database.get_table("modifiers")
        file_table = database.get_table("files")

        
        file_path = self.interface.name_token.file_name
        _, file_name = split_path_and_file_name(file_path)


        object_id = database.save_object(self.interface)
        header_saver = FnHeaderSaver(database, self.interface.fn_headers)
        header_ids = header_saver.save_header_ids()

        name_token = self.interface.name_token
        public_token = self.interface.public_token
        acyclic_token = self.interface.acyclic_token

        interface_table.insert(
            object_id,
            current_module_id,
            name_token,
            header_ids
        )
        type_name_table.insert(
            name_token,
            "interface",
            current_module_id,
            object_id
        )
        header_saver.save_headers()

        mods = []
        for tok in [acyclic_token, public_token]:
            if tok:
                mods.append(tok)
        if len(mods) > 0:
            modifier_table.insert(
                object_id,
                mods
            )

        if file_table.is_file_defined(object_id, file_name):
            raise Exception(f"INTERNAL ERROR: file {file_path} has been processed already")
        if not file_table.is_file_defined(current_module_id, file_name):
            file_table.insert(file_name, current_module_id)
