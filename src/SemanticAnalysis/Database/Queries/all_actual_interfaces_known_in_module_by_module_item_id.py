from SemanticAnalysis.Database.Queries.query import Query
from SemanticAnalysis.Database.Queries.module_items_query import ModuleItemsQuery
from SemanticAnalysis.Database.Queries.import_items_in_module_query import (
    ImportItemsInModuleQuery,
)
from SemanticAnalysis.Database.Queries.actual_imported_items_by_import_statement_item_name_query import (
    ActualImportedItemsByImportStatementItemNameQuery,
)


class AllActualInterfacesKnownInModuleByModuleItemId(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.interface_list = None

    def execute(self, database) -> None:
        typename_table = database.get_table("typenames")
        type_row = typename_table.get_item_by_id(self.object_id)
        current_module_id = type_row.module_id
        self.interface_list = []
        self.add_interfaces_found_in_module(database, current_module_id)
        import_items = database.execute_query(ImportItemsInModuleQuery(current_module_id))
        for import_item in import_items:
            self.add_interfaces_found_in_import(database, import_item)


    def add_interfaces_found_in_module(self, database, current_module_id):
        module_items = database.execute_query(ModuleItemsQuery(current_module_id))
        for module_item in module_items:
            if module_item.object_id == self.object_id:
                continue
            if module_item.category in ["interface"]:
                self.interface_list.append(module_item)

    def add_interfaces_found_in_import(self, database, import_item):
        foreign_module_item_list = self.get_foreign_module_item_list(database, import_item)
        for foreign_module_item in foreign_module_item_list:
            if foreign_module_item.category in ["interface"]:
                self.interface_list.append(foreign_module_item)
    
    def get_foreign_module_item_list(self, database, import_item):
        actual_imported_items = database.execute_query(
            ActualImportedItemsByImportStatementItemNameQuery(self.object_id, import_item)
        )
        foreign_module_item_list = []
        for foreign_module_item in actual_imported_items:
            foreign_module_item_list.append(foreign_module_item)
        return foreign_module_item_list

    def has_next(self) -> bool:
        if self.interface_list is None:
            return False
        return self.index < len(self.interface_list)

    def next(self):
        row = self.interface_list[self.index]
        self.index += 1
        return row
