from SemanticAnalysis.Database.Queries.query import Query
from SemanticAnalysis.Database.Queries.import_items_in_module_from_function_query import ImportItemsInModuleFromFunctionQuery



class MatchingImportItemAliasFromFunction(Query):
    def __init__(self, function_id, item_as_named_in_code) -> None:
        super().__init__(function_id)
        self.items = [] # of type TypeRow from typenames table
        self.item_as_named_in_code = item_as_named_in_code
    
    def execute(self, database) -> None:
        import_statement_item_query = ImportItemsInModuleFromFunctionQuery(self.object_id)
        imported_statement_items = database.execute_query(import_statement_item_query)
        for item in imported_statement_items:
            if item.get_type_name_token().literal == self.item_as_named_in_code:
                self.items.append(item)

    def has_next(self) -> bool:
        return self.index < len(self.items)

    def next(self):
        row = self.items[self.index]
        self.index += 1
        return row
    