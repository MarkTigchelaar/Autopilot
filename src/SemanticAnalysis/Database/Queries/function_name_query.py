from SemanticAnalysis.Database.Queries.query import Query


class FunctionNameQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.name_row = None

    def execute(self, database) -> None:
        function_table = database.get_table("functions")
        function_row = function_table.get_item_by_id(self.object_id)
        header_table = database.get_table("fn_headers")
        header_row = header_table.get_item_by_id(function_row.header_id)
        name_row = FunctionNameRow(function_row.object_id, function_row.header_id, header_row.name_token, function_row.struct_id)
        self.name_row = name_row

    def has_next(self) -> bool:
        return self.name_row is not None

    def next(self):
        temp =  self.name_row
        self.name_row = None
        return temp


class FunctionNameRow:
    def __init__(self, object_id, header_id, name_token, struct_id = None) -> None:
        self.object_id = object_id
        self.header_id = header_id
        self.name_token = name_token
        self.struct_id = struct_id
