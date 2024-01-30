from SemanticAnalysis.Database.SaveData.saver import Saver
from SemanticAnalysis.Database.SaveData.save_statements import StatementSaver
from SemanticAnalysis.Database.SaveData.save_fn_header import FnHeaderSaver
from SemanticAnalysis.AnalysisComponents.analysis_utilities  import split_path_and_file_name

def save_function(analyzer, ast_node):
    function_saver = FunctionSaver(ast_node)
    analyzer.save_item_to_data_store(function_saver)


class FunctionSaver(Saver):
    def __init__(self, function_ast):
        self.function = function_ast
        self.object_id = None


    def save_to_db(self, database):
        current_module_id = database.get_current_module_id()
        type_name_table = database.get_table("typenames")
        function_table = database.get_table("functions")
        file_table = database.get_table("files")
        statement_table = database.get_table("statements")

        file_path = self.function.header.name_token.file_name
        _, file_name = split_path_and_file_name(file_path)

        self.object_id = database.save_object(self.function)

        statement_saver = StatementSaver(self.object_id)
        header_saver = FnHeaderSaver(database, [self.function.header])
        header_ids = header_saver.save_header_ids()
        if len(header_ids) != 1:
            raise Exception("INTERNAL ERROR: function does not have exactly 1 header")

        header_saver.save_headers()
        
        # type_name_table.insert(
        #     self.function.header.name_token,
        #     "function",
        #     current_module_id,
        #     self.object_id
        # )
        function_table.insert(
            self.object_id,
            header_ids[0],
            current_module_id
        )

        statement_saver.save_statements(statement_table, self.function.statements)

        if file_table.is_file_defined(self.object_id, file_name):
            raise Exception(f"INTERNAL ERROR: file {file_path} has been processed already")
        if not file_table.is_file_defined(current_module_id, file_name):
            file_table.insert(file_name, current_module_id)
