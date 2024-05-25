from SemanticAnalysis.Database.Queries.query import Query

class ImportItemsInModuleQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.import_item_list = None

    def execute(self, database) -> None:
        typename_table = database.get_table("typenames")
        import_table = database.get_table("imports")
        type_row = typename_table.get_item_by_id(self.object_id)
        current_module_id = type_row.module_id
        if import_table.module_has_imports(current_module_id):
            import_list = import_table.get_imports_by_module_id(current_module_id)
        else:
            import_list = []
        self.import_item_list = []
        for import_stmt in import_list:
            for import_item in import_stmt.items:
                row = ImportItemsInModuleQueryRow(import_stmt.id, import_item)
                self.import_item_list.append(row)

    def has_next(self) -> bool:
        if self.import_item_list is None:
            return False
        return self.index < len(self.import_item_list)

    def next(self):
        row = self.import_item_list[self.index]
        self.index += 1
        return row


class ImportItemsInModuleQueryRow:
    def __init__(self, statement_id, import_item) -> None:
        self.name_token = import_item.name_token
        self.new_name_token = import_item.new_name_token
        self.import_statement_id = statement_id

    def get_type_name_token(self):
        if self.new_name_token is not None:
            return self.new_name_token
        return self.name_token
