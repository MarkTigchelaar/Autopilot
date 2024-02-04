from SemanticAnalysis.Database.Queries.query import Query

class BuiltInTypeNameQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.type_name = None

    def execute(self, database) -> None:
        typename_table = database.get_table("typenames")
        type_row = typename_table.get_item_by_id(self.object_id)
        self.type_name = type_row.category

    def has_next(self) -> bool:
        return self.type_name is not None

    def next(self):
        temp =  self.type_name
        self.type_name = None
        return temp