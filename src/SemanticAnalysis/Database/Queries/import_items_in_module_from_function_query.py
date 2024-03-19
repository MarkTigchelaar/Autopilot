from SemanticAnalysis.Database.Queries.query import Query
from SemanticAnalysis.Database.Queries.import_items_in_module_query import ImportItemsInModuleQuery

class ImportItemsInModuleFromFunctionQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.import_item_query_result = None

    def execute(self, database) -> None:
        function_table = database.get_table("functions")
        function_row = function_table.get_item_by_id(self.object_id)
        raw_import_query = ImportItemsInModuleQuery(function_row.header_id)
        self.import_item_query_result = database.execute_query(raw_import_query)

    def has_next(self) -> bool:
        return self.import_item_query_result.has_next()
    
    def next(self):
        return self.import_item_query_result.next()
