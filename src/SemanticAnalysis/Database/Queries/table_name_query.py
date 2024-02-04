from SemanticAnalysis.Database.Queries.query import Query

class TableNameQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.table_name = None

    def execute(self, database) -> None:
        self.table_name = [database.get_tablename_for_object(self.object_id)]

    def has_next(self) -> bool:
        if self.table_name is None:
            return False
        return self.index < len(self.table_name)

    def next(self):
        row = self.table_name[self.index]
        self.index += 1
        return row