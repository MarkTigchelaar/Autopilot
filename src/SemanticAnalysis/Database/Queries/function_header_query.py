from SemanticAnalysis.Database.Queries.query import Query


class FunctionHeaderQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.header = None

    def execute(self, database) -> None:
        function_table = database.get_table("functions")
        fn_header_table = database.get_table("fn_headers")
        function_row = function_table.get_item_by_id(self.object_id)
        self.header = fn_header_table.get_item_by_id(function_row.header_id)

    def has_next(self) -> bool:
        if self.header is None:
            return False
        return True

    def next(self):
        row = self.header
        self.header = None
        return row
