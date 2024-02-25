from SemanticAnalysis.Database.Queries.query import Query

class StructNameQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.struct_row = None

    def execute(self, database) -> None:
        struct_table = database.get_table("structs")
        self.struct_row = struct_table.get_item_by_id(self.object_id)

    def has_next(self) -> bool:
        return self.struct_row is not None

    def next(self):
        temp =  self.struct_row
        self.struct_row = None
        return temp