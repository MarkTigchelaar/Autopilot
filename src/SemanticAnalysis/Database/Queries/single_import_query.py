from SemanticAnalysis.Database.Queries.query import Query


class SingleImportQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.import_row = None

    def execute(self, database) -> None:
        import_table = database.get_table("imports")
        self.import_row = import_table.get_row_by_id(self.object_id)

    def has_next(self) -> bool:
        return self.import_row is not None

    def next(self):
        temp =  self.import_row
        self.import_row = None
        return temp
