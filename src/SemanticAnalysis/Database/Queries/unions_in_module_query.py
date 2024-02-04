from SemanticAnalysis.Database.Queries.query import Query
from SemanticAnalysis.Database.Queries.enumerables_in_module import EnumerablesInModuleQuery

class UnionsInModuleQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.unions = None

    def execute(self, database) -> None:
        enumerables = database.execute_query(EnumerablesInModuleQuery(self.object_id))
        self.unions = [row for row in enumerables if row.category == "union"]


    def has_next(self) -> bool:
        if self.unions is None:
            return False
        return self.index < len(self.unions)

    def next(self):
        row = self.unions[self.index]
        self.index += 1
        return row
