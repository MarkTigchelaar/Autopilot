from SemanticAnalysis.Database.Queries.query import Query
from SemanticAnalysis.Database.Queries.current_module_id_query import CurrentModuleIdQueryQuery
class StructsInModuleQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.structs = None

    def execute(self, database) -> None:
        current_module_id = database.execute_query(CurrentModuleIdQueryQuery(self.object_id)).next()
        struct_table = database.get_table("structs")
        if struct_table.is_module_id_defined(current_module_id):
            structs = struct_table.get_items_by_module_id(current_module_id)
        else:
            structs = list()
        self.structs = structs

    def has_next(self) -> bool:
        if self.structs is None:
            return False
        return self.index < len(self.structs)

    def next(self):
        row = self.structs[self.index]
        self.index += 1
        return row
