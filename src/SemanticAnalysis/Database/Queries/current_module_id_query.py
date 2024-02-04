from SemanticAnalysis.Database.Queries.query import Query


class CurrentModuleIdQueryQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.current_module_id = None

    def execute(self, database) -> None:
        typename_table = database.get_table("typenames")
        type_row = typename_table.get_item_by_id(self.object_id)
        self.current_module_id = type_row.module_id

    def has_next(self) -> bool:
        return self.current_module_id is not None

    def next(self):
        temp =  self.current_module_id
        self.current_module_id = None
        return temp
