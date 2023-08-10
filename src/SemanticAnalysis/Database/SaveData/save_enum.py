from SemanticAnalysis.Database.SaveData.saver import Saver


def save_enum(analyzer, ast_node):
    enum_saver = EnumSaver(ast_node)
    analyzer.save_item_to_data_store(enum_saver)


class EnumSaver(Saver):
    def __init__(self, enum_ast):
        self.enum = enum_ast

    def save_to_db(self, database):
        name = self.enum.name
        items = self.enum.item_list
        contained_type = self.enum.general_type
        public_token = self.enum.public_token

        current_module_id = database.get_current_module_id()
        object_id = database.save_object(self.enum)
        type_name_table = database.get_table("typenames")
        enumerable_table = database.get_table("enumerables")
        modifier_table = database.get_table("modifiers")

        type_name_table.insert(
            name,
            "enum",
            current_module_id,
            object_id
        )
        enumerable_table.insert(
            object_id,
            contained_type,
            items
        )
        modifier_table.insert(
            object_id,
            [public_token]
        )
