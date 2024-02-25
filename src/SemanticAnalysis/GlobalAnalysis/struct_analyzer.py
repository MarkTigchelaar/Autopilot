import ErrorHandling.semantic_error_messages as ErrMsg
from SemanticAnalysis.Database.Queries.module_items_query import ModuleItemsQuery
# from SemanticAnalysis.Database.Queries.interface_header_query import (
#     InterfaceHeaderQuery,
# )
from SemanticAnalysis.Database.Queries.struct_name_query import StructNameQuery
# from SemanticAnalysis.Database.Queries.interface_name_query import InterfaceNameQuery
from SemanticAnalysis.Database.Queries.import_items_in_module_query import (
    ImportItemsInModuleQuery,
)
from SemanticAnalysis.Database.Queries.all_actual_interfaces_known_in_module_by_module_item_id import (
    AllActualInterfacesKnownInModuleByModuleItemId
)
# from SemanticAnalysis.Database.Queries.actual_imported_items_by_import_statement_item_name_query import (
#     ActualImportedItemsByImportStatementItemNameQuery,
# )
# from SemanticAnalysis.Database.Queries.built_in_typename_query import (
#     BuiltInTypeNameQuery,
# )
# from keywords import is_primitive_type

OK_TYPES = ["struct", "enum", "union", "defined_type", "interface"]
FORBIDDEN_TYPES = ["error"]

class StructAnalyzer:
    def __init__(self, database, error_manager):
        self.database = database
        self.error_manager = error_manager
        self.object_id = None

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)

    def analyze(self, object_id):
        self.object_id = object_id
        self.check_name_collisions_in_module()
        self.check_name_collisions_in_imports()
        self.check_interface_list()


    def check_name_collisions_in_module(self):
        module_items = self.database.execute_query(ModuleItemsQuery(self.object_id))
        struct_row = self.database.execute_query(
            StructNameQuery(self.object_id)
        ).next()
        for module_item in module_items:
            if module_item.object_id <= struct_row.object_id:
                continue
            if module_item.name_token.literal == struct_row.name_token.literal:
                self.add_error(
                    struct_row.name_token,
                    ErrMsg.STRUCT_NAME_COLLIDES_WITH_MODULE_ITEM,
                    module_item.name_token,
                )
    
    def check_name_collisions_in_imports(self):
        import_items = self.database.execute_query(
            ImportItemsInModuleQuery(self.object_id)
        )
        struct_row = self.database.execute_query(
            StructNameQuery(self.object_id)
        ).next()
        for import_item in import_items:
            name_token = (
                import_item.new_name_token
                if import_item.new_name_token
                else import_item.name_token
            )
            if name_token.literal == struct_row.name_token.literal:
                self.add_error(
                    struct_row.name_token,
                    ErrMsg.STRUCT_NAME_COLLIDES_WITH_IMPORT,
                    name_token,
                )

    def check_interface_list(self):
        struct_row = self.database.execute_query(
            StructNameQuery(self.object_id)
        ).next()
        # check against all interfaces in module and in imports
        # reuse actual imported items query, and add in module stuff, then filter out non-interfaces
        # Stuff all of this into a new query
        all_known_interfaces = self.database.execute_query(
            AllActualInterfacesKnownInModuleByModuleItemId(self.object_id)
        )
        for interface in all_known_interfaces:
            self.check_interface(struct_row, interface)

    def check_interface(self, struct_row, interface):
        for interface_name in struct_row.interfaces:
            if interface_name.literal == interface.name_token.literal:
                if found:
                    self.add_error(
                        struct_row.name_token,
                        ErrMsg.STRUCT_INTERFACE_MATCHES_TO_MULTIPLE_INTERFACES,
                        interface.name_token,
                    )
                found = True
            


"""
,
    {
        "general_component" : "structs without methods checks",
        "test_manifest_file" : "../TestFiles/SemanticAnalyzerTests/GlobalTests/struct_no_method_checks.json"
    }
"""