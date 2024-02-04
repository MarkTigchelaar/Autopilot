from SemanticAnalysis.Database.Queries.query import Query


class InterfaceHeaderQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.header_list = None

    def execute(self, database) -> None:
        interface_table = database.get_table("interfaces")
        fn_header_table = database.get_table("fn_headers")
        interface_row = interface_table.get_item_by_id(self.object_id)
        self.header_list = [
            fn_header_table.get_item_by_id(header_id) for header_id in interface_row.fn_header_ids
        ]

    def has_next(self) -> bool:
        if self.header_list is None:
            return False
        return self.index < len(self.header_list)

    def next(self):
        row = self.header_list[self.index]
        self.index += 1
        return row