from SemanticAnalysis.Database.SaveData.saver import Saver
from SemanticAnalysis.Database.SaveData.save_statements import StatementSaver
from SemanticAnalysis.AnalysisComponents.analysis_utilities  import split_path_and_file_name

def save_unittest(analyzer, ast_node):
    unittest_saver = UnittestSaver(ast_node)
    analyzer.save_item_to_data_store(unittest_saver)


class UnittestSaver(Saver):
    def __init__(self, unittest_ast):
        self.unittest = unittest_ast
        self.object_id = None

    def save_to_db(self, database):
        current_module_id = database.get_current_module_id()
        type_name_table = database.get_table("typenames")
        file_table = database.get_table("files")
        statement_table = database.get_table("statements")

        file_path = self.unittest.name.file_name
        _, file_name = split_path_and_file_name(file_path)

        self.object_id = database.save_object(self.unittest)
        statement_saver = StatementSaver(self.object_id)

        type_name_table.insert(
            self.unittest.name,
            "unittest",
            current_module_id,
            self.object_id
        )

        statement_saver.save_statements(statement_table, self.unittest.statements, 0)

        if file_table.is_file_defined(self.object_id, file_name):
            raise Exception(f"INTERNAL ERROR: file {file_path} has been processed already")
        if not file_table.is_file_defined(current_module_id, file_name):
            file_table.insert(file_name, current_module_id)
