from SemanticAnalysis.Database.Queries.query import Query
from SemanticAnalysis.Database.Queries.module_items_query import ModuleItemsQuery
from SemanticAnalysis.Database.Queries.actual_imported_items_by_import_statement_item_name_from_function_query import ActualImportedItemsByImportStatementItemNameFromFunctionQuery
from SemanticAnalysis.Database.Queries.function_name_query import FunctionNameQuery
from SemanticAnalysis.Database.Queries.import_items_in_module_from_function_query import ImportItemsInModuleFromFunctionQuery



class ModuleAndImportedItemsFromCallerFunctionIdAndCalleeNameQuery(Query):
    def __init__(self, function_id, called_function_name) -> None:
        super().__init__(function_id)
        self.items = [] # of type TypeRow from typenames table
        self.called_function_name = called_function_name

    def execute(self, database) -> None:
        header_query = FunctionNameQuery(self.object_id)
        function_data = database.execute_query(header_query).next()
        function_header_id = function_data.header_id

        module_items = self.get_module_items(function_header_id, database)
        imported_items = self.get_modules_matching_imported_items(database)

        for item in module_items:
            self.items.append(item)
        for item in imported_items:
            self.items.append(item)
        


    def get_module_items(self, function_header_id, database):
        module_item_query = ModuleItemsQuery(function_header_id)
        return database.execute_query(module_item_query)
    

    def get_modules_matching_imported_items(self, database):
        import_statement_item_query = ImportItemsInModuleFromFunctionQuery(self.object_id)
        imported_statement_items = database.execute_query(import_statement_item_query)
        import_statement_itemlist = list()
        for item in imported_statement_items:
            if item.get_type_name_token().literal == self.called_function_name:
                import_statement_itemlist.append(item)
        
        imported_items = list()
        for import_list_item in import_statement_itemlist:
            imported_item_query = ActualImportedItemsByImportStatementItemNameFromFunctionQuery(self.object_id, import_list_item)
            matching_imported_items = database.execute_query(imported_item_query)
            for matching_item in matching_imported_items:
                imported_items.append(matching_item)
        return imported_items


    def has_next(self) -> bool:
        return self.index < len(self.items)

    def next(self):
        row = self.items[self.index]
        self.index += 1
        return row
