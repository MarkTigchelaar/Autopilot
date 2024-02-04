import ErrorHandling.semantic_error_messages as ErrMsg
from SemanticAnalysis.Database.Queries.module_items_query import ModuleItemsQuery
from SemanticAnalysis.Database.Queries.interface_header_query import (
    InterfaceHeaderQuery,
)
from SemanticAnalysis.Database.Queries.interface_name_query import InterfaceNameQuery
from SemanticAnalysis.Database.Queries.import_items_in_module_query import (
    ImportItemsInModuleQuery,
)
from SemanticAnalysis.Database.Queries.imported_items_by_import_statement_item_name_query import (
    ImportedItemsByImportStatementItemNameQuery,
)
from SemanticAnalysis.Database.Queries.built_in_typename_query import (
    BuiltInTypeNameQuery,
)
from keywords import is_primitive_type

OK_TYPES = ["struct", "enum", "union", "defined_type", "interface"]
FORBIDDEN_TYPES = ["error"]


class InterfaceAnalyzer:
    def __init__(self, database, error_manager):
        self.database = database
        self.error_manager = error_manager
        self.object_id = None

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)

    def analyze(self, object_id):
        self.object_id = object_id
        self.check_name_collisions()
        self.check_method_type_useage()

    def check_name_collisions(self):
        self.check_name_collisions_in_module()
        self.check_name_collisions_in_imports()

    def check_name_collisions_in_module(self):
        module_items = self.database.execute_query(ModuleItemsQuery(self.object_id))
        interface_row = self.database.execute_query(
            InterfaceNameQuery(self.object_id)
        ).next()
        for module_item in module_items:
            if module_item.object_id <= interface_row.object_id:
                continue
            if module_item.name_token.literal == interface_row.name_token.literal:
                self.add_error(
                    interface_row.name_token,
                    ErrMsg.INTERFACE_NAME_COLLIDES_WITH_MODULE_ITEM,
                    module_item.name_token,
                )

    def check_name_collisions_in_imports(self):
        import_items = self.database.execute_query(
            ImportItemsInModuleQuery(self.object_id)
        )
        interface_row = self.database.execute_query(
            InterfaceNameQuery(self.object_id)
        ).next()
        for import_item in import_items:
            name_token = (
                import_item.new_name_token
                if import_item.new_name_token
                else import_item.name_token
            )
            if name_token.literal == interface_row.name_token.literal:
                self.add_error(
                    interface_row.name_token,
                    ErrMsg.INTERFACE_NAME_COLLIDES_WITH_IMPORT,
                    name_token,
                )

    def check_method_type_useage(self):
        header_list = self.database.execute_query(InterfaceHeaderQuery(self.object_id))
        for header in header_list:
            for arg in header.get_args():
                arg_type_token = arg.get_type()
                if is_primitive_type(arg_type_token):
                    continue
                if not self.check_module_item_types(
                    arg_type_token, ErrMsg.INVALID_FUNCTION_ARG_TYPE
                ):
                    self.check_imported_types_for_arg(
                        arg_type_token, ErrMsg.INVALID_FUNCTION_ARG_TYPE
                    )
            self.check_return_type(header.return_type_token)

    def check_return_type(self, return_type_token):
        if return_type_token is None:
            return
        if is_primitive_type(return_type_token):
            return
        if not self.check_module_item_types(
            return_type_token, ErrMsg.INVALID_FUNCTION_RETURN_TYPE
        ):
            self.check_imported_types_for_arg(
                return_type_token, ErrMsg.INVALID_FUNCTION_RETURN_TYPE
            )

    def check_module_item_types(self, arg_type_token, error_message):

        module_items = self.database.execute_query(ModuleItemsQuery(self.object_id))
        for module_item in module_items:
            if module_item.name_token.literal != arg_type_token.literal:
                continue
            item_object_id = module_item.object_id

            type_name = self.database.execute_query(
                BuiltInTypeNameQuery(item_object_id)
            ).next()

            if type_name in FORBIDDEN_TYPES:
                self.add_error(arg_type_token, error_message)
                return True
            elif type_name in OK_TYPES:
                if module_item.name_token.literal == arg_type_token.literal:
                    return True

        return False

    def check_imported_types_for_arg(self, arg_type_token, error_message):
        import_items = self.database.execute_query(
            ImportItemsInModuleQuery(self.object_id)
        )
        for import_item in import_items:
            name_token = (
                import_item.new_name_token
                if import_item.new_name_token
                else import_item.name_token
            )
            if name_token.literal != arg_type_token.literal:
                continue
            # Could have duplicate names coming in from more than one import statement
            # check them all
            items_from_imported_module = self.database.execute_query(
                ImportedItemsByImportStatementItemNameQuery(
                    import_item.import_statement_id, import_item.name_token
                )
            )
            for item in items_from_imported_module:
                if item.name_token.literal != arg_type_token.literal:
                    continue
                item_object_id = item.object_id
                type_name = self.database.execute_query(
                    BuiltInTypeNameQuery(item_object_id)
                ).next()
                if type_name in FORBIDDEN_TYPES:
                    self.add_error(arg_type_token, error_message)
                    return
                elif type_name in OK_TYPES:
                    return
