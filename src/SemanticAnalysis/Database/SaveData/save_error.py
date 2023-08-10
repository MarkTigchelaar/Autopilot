from SemanticAnalysis.Database.SaveData.saver import Saver


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

        type_name_table.insert(
            name,
            "error",
            current_module_id,
            object_id
        )
        enumerable_table.insert(
            object_id,
            items
        )
        modifier_table.insert(
            object_id,
            [public_token]
        )
