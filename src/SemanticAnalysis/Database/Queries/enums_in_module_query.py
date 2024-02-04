from SemanticAnalysis.Database.Queries.query import Query
from SemanticAnalysis.Database.Queries.enumerables_in_module import EnumerablesInModuleQuery

class EnumsInModuleQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.enums = None

    def execute(self, database) -> None:
        enumerables = database.execute_query(EnumerablesInModuleQuery(self.object_id))
        self.enums = [row for row in enumerables if row.category == "enum"]


    def has_next(self) -> bool:
        if self.enums is None:
            return False
        return self.index < len(self.enums)

    def next(self):
        row = self.enums[self.index]
        self.index += 1
        return row
