from SemanticAnalysis.Database.Queries.query import Query
from SemanticAnalysis.Database.Queries.actual_imported_items_by_import_statement_item_name_query import (
    ActualImportedItemsByImportStatementItemNameQuery,
)

class ActualImportedItemsByImportStatementItemNameFromFunctionQuery(Query):
    def __init__(self, object_id, import_item) -> None:
        super().__init__(object_id)
        self.sub_query_results = None
        self.import_item = import_item

    def execute(self, database) -> None:
        function_table = database.get_table("functions")
        function_row = function_table.get_item_by_id(self.object_id)
        header_id = function_row.header_id
        sub_query = ActualImportedItemsByImportStatementItemNameQuery(header_id, self.import_item)
        self.sub_query_results = database.execute_query(sub_query)

    def has_next(self) -> bool:
        return self.sub_query_results.has_next()

    def next(self):
        return self.sub_query_results.next()
