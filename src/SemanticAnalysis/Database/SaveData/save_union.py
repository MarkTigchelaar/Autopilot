from SemanticAnalysis.Database.SaveData.saver import Saver


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

        type_name_table.insert(
            name,
            "union",
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
