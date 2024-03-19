import ErrorHandling.semantic_error_messages as ErrMsg
from SemanticAnalysis.Database.Queries.module_items_from_function_query import (
    ModuleItemsFromFunctionQuery,
)
from SemanticAnalysis.Database.Queries.import_items_in_module_from_function_query import (
    ImportItemsInModuleFromFunctionQuery,
)
from SemanticAnalysis.Database.Queries.function_header_query import (
    FunctionHeaderQuery,
)
from SemanticAnalysis.Database.Queries.function_name_query import FunctionNameQuery
from keywords import is_primitive_type

from SemanticAnalysis.Database.Queries.module_items_query import ModuleItemsQuery

from SemanticAnalysis.Database.Queries.import_items_in_module_query import (
    ImportItemsInModuleQuery,
)
from SemanticAnalysis.Database.Queries.actual_imported_items_by_import_statement_item_name_from_function_query import (
    ActualImportedItemsByImportStatementItemNameFromFunctionQuery,
)
from SemanticAnalysis.Database.Queries.built_in_typename_query import (
    BuiltInTypeNameQuery,
)

OK_TYPES = ["struct", "enum", "union", "defined_type", "interface"]
FORBIDDEN_TYPES = ["error"]

class FunctionAnalyzer:
    def __init__(self, database, error_manager):
        self.database = database
        self.error_manager = error_manager
        self.object_id = None
        self.is_main = False

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)

        # Obvious things:
        # Name collisions
        # arg and return type analysis
        # Then its all statement analysis!
        # Statement analysis needs:
        # a statement saver
        # statement table
        # query class
        # expression analyzer + table?

    def analyze(self, object_id):
        self.is_main = False
        self.object_id = object_id
        self.check_for_main_function()
        self.check_name_collisions_in_module()
        self.check_name_collisions_in_imports()
        self.check_args_and_return_type()
        self.analyze_function_body()

    def check_for_main_function(self):
        function_info_row = self.database.execute_query(
            FunctionNameQuery(self.object_id)
        ).next()
        if function_info_row.name_token.literal == "main":
            self.is_main = True

    def check_name_collisions_in_module(self):
        module_items = self.database.execute_query(
            ModuleItemsFromFunctionQuery(self.object_id)
        )
        function_info_row = self.database.execute_query(
            FunctionNameQuery(self.object_id)
        ).next()
        for module_item in module_items:
            if module_item.object_id <= function_info_row.object_id:
                continue
            elif module_item.object_id == function_info_row.header_id:
                continue
            # Account for:
            # main inside main module
            # methods having same name of methods in different tpye (this is ok)
            # functions having same names of other tpyes (normal, covered here)

            if module_item.name_token.literal == function_info_row.name_token.literal:
                if self.is_main_module(module_item) and self.is_main:
                    continue
                if self.is_method(function_info_row):
                    # different structs can have same method names,
                    # especially when they implement the same interface
                    # methods can have same names as functions
                    continue
                self.add_error(
                    function_info_row.name_token,
                    ErrMsg.FUNCTION_NAME_COLLIDES_WITH_MODULE_ITEM,
                    module_item.name_token,
                )

    def is_main_module(self, module_item):
        return (
            module_item.name_token.literal == "main"
            and module_item.category == "module"
        )

    def is_method(self, function_info_row):
        return function_info_row.struct_id is not None

    def check_name_collisions_in_imports(self):
        import_items = self.database.execute_query(
            ImportItemsInModuleFromFunctionQuery(self.object_id)
        )
        function_row = self.database.execute_query(
            FunctionNameQuery(self.object_id)
        ).next()
        for import_item in import_items:
            name_token = (
                import_item.new_name_token
                if import_item.new_name_token
                else import_item.name_token
            )
            if name_token.literal == function_row.name_token.literal:
                self.add_error(
                    function_row.name_token,
                    ErrMsg.FUNCTION_NAME_COLLIDES_WITH_IMPORT,
                    name_token,
                )

    # This is the same code as is used in interface analyzer, migh be a good idea to pull it out
    # and into a shared class or shared functions
    def check_args_and_return_type(self):
        header_list = self.database.execute_query(FunctionHeaderQuery(self.object_id))
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

        module_items = self.database.execute_query(ModuleItemsFromFunctionQuery(self.object_id))
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
            ImportItemsInModuleFromFunctionQuery(self.object_id)
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
            # check all of them

            items_from_imported_module = self.database.execute_query(
                ActualImportedItemsByImportStatementItemNameFromFunctionQuery(
                    self.object_id, import_item
                )
            )
            if not items_from_imported_module.has_next():
                raise Exception(
                    "INTERNAL ERROR: No items found for import statement, should have been caught in import analyzer"
                )
            for item in items_from_imported_module:
                # BUG?: new names are not being checked, only the original name
                # line up new names also with the correct
                # FIX IN PLACE, add tests to check that analyzer is not confused by name aliasing
                if item.name_token.literal != import_item.name_token.literal:
                    continue
                item_object_id = item.object_id
                type_name = self.database.execute_query(
                    BuiltInTypeNameQuery(item_object_id)
                ).next()
                if type_name in FORBIDDEN_TYPES:
                    # Be sure to use which ever name is being used in the function header
                    # so name_token is used here, not arg_type_token, which could be the new name
                    self.add_error(arg_type_token, error_message, item.name_token)
                    return
                elif type_name in OK_TYPES:
                    return


    def analyze_function_body(self):
        pass


"""
TODO list:
Check that argument types are defined somewhere
Check that function name has no collisions
Check the variable names are defined in their scope
Check types for argument re assignment
check types of expressions
Check method and function calls
Register current function as caller of any called functions to later check inline / acyclic rules
Check fields and methods of types referenced in function
Check arguments to other functions and methods
Enforce enumerable type rules, like with switch statements for unions
Enforce optional variable rules.
Enforce that collections return Results or Optionals if guarantee of membership is not present
Check that Errors in results have valid fields
Check that break statements that refer to labels have labels that exist
Check that labels have no name collisions
Check assignment types, for let, and var
Check if expressions violate int / float promotion rules
Check that function / method calls are public
"""
