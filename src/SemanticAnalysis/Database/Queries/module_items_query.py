from SemanticAnalysis.Database.Queries.query import Query

class ModuleItemsQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.module_items = None

    def execute(self, database) -> None:
        typename_table = database.get_table("typenames")
        type_row = typename_table.get_item_by_id(self.object_id)
        current_module_id = type_row.module_id
        self.module_items = typename_table.get_items_by_module_id(current_module_id)

    def has_next(self) -> bool:
        if self.module_items is None:
            return False
        return self.index < len(self.module_items)

    def next(self):
        row = self.module_items[self.index]
        self.index += 1
        return row
