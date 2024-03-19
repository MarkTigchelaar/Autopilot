from SemanticAnalysis.Database.Queries.query import Query
from SemanticAnalysis.Database.Queries.module_items_query import ModuleItemsQuery

class ModuleItemsFromFunctionQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.module_query = None

    def execute(self, database) -> None:
        function_table = database.get_table("functions")
        function_row = function_table.get_item_by_id(self.object_id)
        #header_table = database.get_table("fn_headers")
        #header_row = header_table.get_item_by_id(function_row.header_id)
        #self.name_token = header_row.name_token
        raw_module_query = ModuleItemsQuery(function_row.header_id)
        self.module_query = database.execute_query(raw_module_query)

    def has_next(self) -> bool:
        return self.module_query.has_next()

    def next(self):
        return self.module_query.next()
