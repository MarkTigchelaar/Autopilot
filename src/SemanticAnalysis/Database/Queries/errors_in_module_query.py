from SemanticAnalysis.Database.Queries.query import Query
from SemanticAnalysis.Database.Queries.enumerables_in_module import EnumerablesInModuleQuery

class ErrorsInModuleQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.errors = None

    def execute(self, database) -> None:
        enumerables = database.execute_query(EnumerablesInModuleQuery(self.object_id))
        self.errors = [row for row in enumerables if row.category == "error"]


    def has_next(self) -> bool:
        if self.errors is None:
            return False
        return self.index < len(self.errors)

    def next(self):
        row = self.errors[self.index]
        self.index += 1
        return row
