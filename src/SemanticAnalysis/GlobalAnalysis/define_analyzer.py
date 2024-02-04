import ErrorHandling.semantic_error_messages as ErrMsg
from keywords import is_primitive_type
from symbols import OPTION, RESULT
import symbols
from SemanticAnalysis.AnalysisComponents.define_statement_dependancy_checker import (
    DefineStatementDependencyChecker,
)
from SemanticAnalysis.Database.Queries.module_items_query import ModuleItemsQuery
from SemanticAnalysis.Database.Queries.import_items_in_module_query import ImportItemsInModuleQuery
from SemanticAnalysis.Database.Queries.single_define_query import SingleDefineQuery
from SemanticAnalysis.Database.Queries.defines_in_module_query import (
    DefinesInModuleQuery,
)


class DefineAnalyzer:
    def __init__(self, database, error_manager):
        self.database = database
        self.error_manager = error_manager
        self.object_id = None

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)

    def analyze(self, object_id):
        self.object_id = object_id
        self.check_for_new_typename_collisions()
        self.check_other_defines_for_same_components()
        self.check_if_is_function_type_with_no_args_no_return_type()
        undefined_items = self.check_items_in_definition_are_defined()

        self.enforce_define_rules(undefined_items)

    def check_for_new_typename_collisions(self):
        module_items = self.database.execute_query(ModuleItemsQuery(self.object_id))
        for module_item in module_items:
            self.check_module_item(module_item)

        imports = self.database.execute_query(ImportItemsInModuleQuery(self.object_id))
        for import_item in imports:
            self.check_import_item(import_item)

    def check_module_item(self, module_item):
        define_row = self.database.execute_query(
            SingleDefineQuery(self.object_id)
        ).next()
        if module_item.object_id <= define_row.object_id:
            return
        if module_item.name_token.literal == define_row.new_type_name_token.literal:
            self.add_error(
                define_row.new_type_name_token,
                ErrMsg.DEFINE_NEW_NAME_COLLISION,
                module_item.name_token,
            )

    def check_import_item(self, import_item):
        name_token = (
            import_item.new_name_token
            if import_item.new_name_token
            else import_item.name_token
        )
        define_row = self.database.execute_query(
            SingleDefineQuery(self.object_id)
        ).next()
        if name_token.literal == define_row.new_type_name_token.literal:
            self.add_error(
                define_row.new_type_name_token,
                ErrMsg.DEFINE_NEW_NAME_COLLISION_W_IMPORT,
                name_token,
            )

    def check_other_defines_for_same_components(self):
        define_row = self.database.execute_query(
            SingleDefineQuery(self.object_id)
        ).next()
        other_defines = self.database.execute_query(
            DefinesInModuleQuery(self.object_id)
        )
        for other_define in other_defines:
            if define_row.object_id >= other_define.object_id:
                continue
            if (
                define_row.built_in_type_token.literal
                != other_define.built_in_type_token.literal
            ):
                continue
            self.check_key_type(define_row, other_define)
            self.check_value_type(define_row, other_define)
            self.check_optional_or_result_type(define_row, other_define)
            self.check_function_signature(define_row, other_define)

    def check_key_type(self, define_row, other_define):
        if define_row.key_type and other_define.key_type:
            if define_row.key_type.literal == other_define.key_type.literal:
                if define_row.value_type and other_define.value_type:
                    if define_row.value_type.literal == other_define.value_type.literal:
                        self.add_error(
                            define_row.new_type_name_token,
                            ErrMsg.DEFINE_USES_SAME_COMPONENTS,
                            other_define.new_type_name_token,
                        )

    def check_value_type(self, define_row, other_define):
        if define_row.arg_list or other_define.arg_list:
            return
        if define_row.key_type or other_define.key_type:
            return
        if define_row.result_type or other_define.result_type:
            return
        if not define_row.value_type and other_define.value_type:
            return
        if define_row.built_in_type_token.type_symbol in (OPTION, RESULT):
            return
        if define_row.value_type.literal == other_define.value_type.literal:
            self.add_error(
                define_row.new_type_name_token,
                ErrMsg.DEFINE_USES_SAME_COMPONENTS,
                other_define.new_type_name_token,
            )

    def check_optional_or_result_type(self, define_row, other_define):
        if not (define_row.value_type and other_define.value_type):
            return
        if define_row.built_in_type_token.type_symbol not in (OPTION, RESULT):
            return
        if not (define_row.result_type and other_define.result_type):
            self.check_optional(define_row, other_define)
            return
        if define_row.result_type.type_symbol != other_define.result_type.type_symbol:
            return
        if define_row.value_type.literal != other_define.value_type.literal:
            return
        if define_row.result_type.literal == other_define.result_type.literal:
            self.add_error(
                define_row.new_type_name_token,
                ErrMsg.DEFINE_USES_SAME_COMPONENTS,
                other_define.new_type_name_token,
            )

    def check_optional(self, define_row, other_define):
        if define_row.built_in_type_token.type_symbol != OPTION:
            return
        if define_row.value_type.literal != other_define.value_type.literal:
            return
        self.add_error(
            define_row.new_type_name_token,
            ErrMsg.DEFINE_USES_SAME_COMPONENTS,
            other_define.new_type_name_token,
        )

    def check_function_signature(self, define_row, other_define):
        if not (define_row.arg_list and other_define.arg_list):
            return
        if len(define_row.arg_list) != len(other_define.arg_list):
            return
        if not (
            (define_row.value_type and other_define.value_type)
            or (not define_row.value_type and not other_define.value_type)
        ):
            return

        arg_literals = [arg.literal for arg in define_row.arg_list]
        other_arg_literals = [arg.literal for arg in define_row.arg_list]
        arg_literals.sort()
        other_arg_literals.sort()
        same = all(a == b for a, b in zip(arg_literals, other_arg_literals))

        if same and not define_row.value_type and not other_define.value_type:
            self.add_error(
                define_row.new_type_name_token,
                ErrMsg.DEFINE_USES_SAME_COMPONENTS,
                other_define.new_type_name_token,
            )
        elif same and (
            define_row.value_type.literal == other_define.value_type.literal
        ):
            self.add_error(
                define_row.new_type_name_token,
                ErrMsg.DEFINE_USES_SAME_COMPONENTS,
                other_define.new_type_name_token,
            )

    def check_if_is_function_type_with_no_args_no_return_type(self):
        define_row = self.database.execute_query(
            SingleDefineQuery(self.object_id)
        ).next()
        if define_row.key_type:
            return
        if define_row.value_type:
            return
        # not needed, but add just in case
        if define_row.result_type:
            return
        if define_row.arg_list and len(define_row.arg_list) > 0:
            return
        self.add_error(
            define_row.new_type_name_token, ErrMsg.FUNCTION_TYPE_HAS_NO_EFFECT
        )

    def get_items_to_check(self):
        define_row = self.database.execute_query(
            SingleDefineQuery(self.object_id)
        ).next()
        items_to_check = [
            define_row.key_type,
            define_row.value_type,
            define_row.result_type,
        ]
        if define_row.arg_list:
            items_to_check.extend(define_row.arg_list)
        items_to_check = [
            token for token in items_to_check if self.is_not_primitive_or_none(token)
        ]
        return items_to_check

    def check_items_in_same_module(self, items_to_check):
        module_items = self.database.execute_query(ModuleItemsQuery(self.object_id))
        define_row = self.database.execute_query(
            SingleDefineQuery(self.object_id)
        ).next()
        for module_item in module_items:
            if len(items_to_check) < 1:
                return
            for i in reversed(range(len(items_to_check))):
                defined_item = items_to_check[i]
                if module_item.object_id == define_row.object_id:
                    continue
                if module_item.name_token.literal == defined_item.literal:
                    items_to_check.pop(i)

    def check_items_in_imports(self, items_to_check):
        imports = self.database.execute_query(ImportItemsInModuleQuery(self.object_id))
        for imported_item in imports:
            if len(items_to_check) < 1:
                return
            for i in reversed(range(len(items_to_check))):
                defined_item = items_to_check[i]

                if len(items_to_check) < 1:
                    return
                if imported_item.new_name_token:
                    if imported_item.new_name_token.literal == defined_item.literal:
                        items_to_check.pop(i)
                elif imported_item.name_token:
                    if imported_item.name_token.literal == defined_item.literal:
                        items_to_check.pop(i)

    def check_items_in_definition_are_defined(self):
        items_to_check = self.get_items_to_check()
        if len(items_to_check) < 1:
            return items_to_check
        self.check_items_in_same_module(items_to_check)
        if len(items_to_check) < 1:
            return items_to_check
        self.check_items_in_imports(items_to_check)
        for undefined_item_token in items_to_check:
            self.add_error(undefined_item_token, ErrMsg.UNDEFINED_ITEM_IN_DEFINE_STMT)

        return items_to_check

    def is_not_primitive_or_none(self, token):
        if token is None:
            return False
        return not is_primitive_type(token)

    def check_that_there_are_no_cycles_in_defined_types(self, undefined_items):
        define_row = self.database.execute_query(
            SingleDefineQuery(self.object_id)
        ).next()
        checker = DefineStatementDependencyChecker(
            undefined_items, self.error_manager, self.database, self.object_id
        )
        checker.check_dag(define_row)

    def enforce_nested_define_rules(self):
        define_row = self.database.execute_query(
            SingleDefineQuery(self.object_id)
        ).next()
        match define_row.built_in_type_token.type_symbol:
            case symbols.LIST:
                self.analyze_define_elements_for_linear_collection_types_default(
                    define_row, ErrMsg.LIST_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.LINKEDLIST:
                self.analyze_define_elements_for_linear_collection_types_default(
                    define_row, ErrMsg.LINKED_LIST_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.VECTOR:
                self.analyze_define_elements_for_linear_collection_types_default(
                    define_row, ErrMsg.VECTOR_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.MAP:
                # for the values in kv pair:
                self.analyze_define_elements_for_linear_collection_types_default(
                    define_row, ErrMsg.MAP_TYPE_VALUE_DEFINE_NESTING_INVALID_DEFINES
                )
                # for keys in kv pair:
                self.analyze_define_elements_for_hash_key_collection_types(
                    define_row, ErrMsg.MAP_TYPE_KEY_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.HASHMAP:
                self.analyze_define_elements_for_linear_collection_types_default(
                    define_row, ErrMsg.HASHMAP_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
                self.analyze_define_elements_for_hash_key_collection_types(
                    define_row, ErrMsg.HASHMAP_TYPE_KEY_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.DICTIONARY:
                self.analyze_define_elements_for_linear_collection_types_default(
                    define_row, ErrMsg.DICT_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
                self.analyze_define_elements_for_hash_key_collection_types(
                    define_row, ErrMsg.DICT_TYPE_KEY_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.SET:
                self.analyze_define_elements_for_hash_collection_types(
                    define_row, ErrMsg.SET_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.HASHSET:
                self.analyze_define_elements_for_hash_collection_types(
                    define_row, ErrMsg.HASHSET_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.TREESET:
                self.analyze_define_elements_for_hash_collection_types(
                    define_row, ErrMsg.TREESET_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.OPTION:
                self.analyze_define_elements_for_option_types(define_row)
            case symbols.RESULT:
                self.analyze_define_elements_for_result_types(define_row)
            case symbols.QUEUE:
                self.analyze_define_elements_for_linear_collection_types_default(
                    define_row, ErrMsg.QUEUE_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.FIFOQUEUE:
                self.analyze_define_elements_for_linear_collection_types_default(
                    define_row, ErrMsg.FIFO_QUEUE_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.DEQUE:
                self.analyze_define_elements_for_linear_collection_types_default(
                    define_row, ErrMsg.DEQUE_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.PRIORITYQUEUE:
                self.analyze_define_elements_for_linear_collection_types_default(
                    define_row, ErrMsg.PRIORITY_QUEUE_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.STACK:
                self.analyze_define_elements_for_linear_collection_types_default(
                    define_row, ErrMsg.STACK_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.FUN:
                self.analyze_define_elements_for_function_types(define_row)
            case _:
                raise Exception(
                    f"INTERNAL ERROR: Invalid define type found: {define_row.built_in_type_token.type_symbol}"
                )

    def analyze_define_elements_for_hash_collection_types(
        self, define_row, error_message
    ):
        types_to_check = {
            "acceptable_user_def_types": ["struct", "interface"],
            "acceptable_define_stmt_types": [],
        }
        self.analyze_define_elements_for_generic_collection_types(
            define_row.value_type,
            define_row.current_module_id,
            error_message,
            types_to_check,
        )

    def analyze_define_elements_for_hash_key_collection_types(
        self, define_row, error_message
    ):
        types_to_check = {
            "acceptable_user_def_types": ["struct", "interface"],
            "acceptable_define_stmt_types": [],
        }
        self.analyze_define_elements_for_generic_collection_types(
            define_row.key_type,
            define_row.current_module_id,
            error_message,
            types_to_check,
        )

    def analyze_define_elements_for_linear_collection_types_default(
        self, define_row, error_message
    ):
        types_to_check = {
            "acceptable_user_def_types": [
                "struct",
                "union",
                "enum",
                "error",
                "interface",
            ],
            "acceptable_define_stmt_types": [
                symbols.FUN,
                symbols.OPTION,
                symbols.RESULT,
            ],
        }
        self.analyze_define_elements_for_generic_collection_types(
            define_row.value_type,
            define_row.current_module_id,
            error_message,
            types_to_check,
        )

    def analyze_define_elements_for_option_types(self, define_row):
        types_to_check = {
            "acceptable_user_def_types": ["struct", "union", "enum", "interface"],
            "acceptable_define_stmt_types": [  # everything except options
                symbols.FUN,
                symbols.RESULT,
                symbols.LIST,
                symbols.LINKEDLIST,
                symbols.VECTOR,
                symbols.SET,
                symbols.HASHSET,
                symbols.TREESET,
                symbols.MAP,
                symbols.HASHMAP,
                symbols.DICTIONARY,
                symbols.QUEUE,
                symbols.FIFOQUEUE,
                symbols.DEQUE,
                symbols.PRIORITYQUEUE,
                symbols.STACK,
            ],
        }
        self.analyze_define_elements_for_generic_collection_types(
            define_row.value_type,
            define_row.current_module_id,
            ErrMsg.OPTION_TYPE_DEFINE_NESTING_INVALID_DEFINES,
            types_to_check,
        )

    def analyze_define_elements_for_result_types(self, define_row):
        types_to_check = {
            "acceptable_user_def_types": ["struct", "union", "enum", "interface"],
            "acceptable_define_stmt_types": [  # everything except results
                symbols.FUN,
                symbols.OPTION,
                symbols.LIST,
                symbols.LINKEDLIST,
                symbols.VECTOR,
                symbols.SET,
                symbols.HASHSET,
                symbols.TREESET,
                symbols.MAP,
                symbols.HASHMAP,
                symbols.DICTIONARY,
                symbols.QUEUE,
                symbols.FIFOQUEUE,
                symbols.DEQUE,
                symbols.PRIORITYQUEUE,
                symbols.STACK,
            ],
        }
        self.analyze_define_elements_for_generic_collection_types(
            define_row.value_type,
            define_row.current_module_id,
            ErrMsg.RESULT_TYPE_DEFINE_NESTING_INVALID_DEFINES,
            types_to_check,
        )

        types_to_check = {
            "acceptable_user_def_types": ["error"],
            "acceptable_define_stmt_types": [],
        }
        self.analyze_define_elements_for_generic_collection_types(
            define_row.result_type,
            define_row.current_module_id,
            ErrMsg.RESULT_TYPE_ERROR_DEFINE_NESTING_INVALID_DEFINES,
            types_to_check,
        )

    def analyze_define_elements_for_function_types(self, define_row):
        types_to_check = {
            "acceptable_user_def_types": [
                "struct",
                "union",
                "enum",
                "error",
                "interface",
            ],
            "acceptable_define_stmt_types": [
                symbols.FUN,
                symbols.OPTION,
                symbols.RESULT,
                symbols.LIST,
                symbols.LINKEDLIST,
                symbols.VECTOR,
                symbols.SET,
                symbols.HASHSET,
                symbols.TREESET,
                symbols.MAP,
                symbols.HASHMAP,
                symbols.DICTIONARY,
                symbols.QUEUE,
                symbols.FIFOQUEUE,
                symbols.DEQUE,
                symbols.PRIORITYQUEUE,
                symbols.STACK,
            ],
        }
        for arg in define_row.arg_list:
            self.analyze_define_elements_for_generic_collection_types(
                arg,
                define_row.current_module_id,
                ErrMsg.FUNCTION_TYPE_ARG_DEFINE_NESTING_INVALID_DEFINES,
                types_to_check,
            )

        # If function has return type
        if define_row.value_type:
            self.analyze_define_elements_for_generic_collection_types(
                define_row.value_type,  # function return type
                define_row.current_module_id,
                ErrMsg.FUNCTION_TYPE_RETURN_VAL_DEFINE_NESTING_INVALID_DEFINES,
                types_to_check,
            )

    def analyze_define_elements_for_generic_collection_types(
        self, contained_type_token, current_module_id, error_message, types_to_check
    ):
        typename_table = self.database.get_table("typenames")
        import_table = self.database.get_table("imports")
        module_table = self.database.get_table("modules")
        modifier_table = self.database.get_table("modifiers")
        if contained_type_token is None:
            raise Exception("INTERNAL ERROR: contained type token is None")
        if is_primitive_type(contained_type_token):
            return
        if typename_table.is_name_defined_in_module(
            contained_type_token.literal, current_module_id
        ):
            type_name_rows = typename_table.get_rows_by_name_and_module(
                contained_type_token.literal, current_module_id
            )
            if len(type_name_rows) != 1:
                return
            type_name_row = type_name_rows[0]
            self.check_for_invalid_nested_defines(
                type_name_row, contained_type_token, error_message, types_to_check
            )
        elif import_table.module_has_imports(current_module_id):
            imports = import_table.get_imports_by_module_id(current_module_id)
            for import_row in imports:
                possible_modules = module_table.get_modules_data_for_name(
                    import_row.imported_module_name_token.literal
                )
                if len(possible_modules) != 1:
                    continue
                    # Is a duplicate, in that case, skip these checks
                    # or, import refers to non existant module, in which case, skip these checks
                imported_module = possible_modules[0]
                self.inspect_import_items_for_define_nesting(
                    import_row,
                    contained_type_token,
                    typename_table,
                    imported_module,
                    modifier_table,
                    error_message,
                    types_to_check,
                )

    def is_public(self, type_name_row, modifier_table):
        if not modifier_table.is_object_defined(type_name_row.object_id):
            return False
        modifier_list = modifier_table.get_modifier_list_by_id(type_name_row.object_id)
        return any(mod.literal == "pub" for mod in modifier_list if modifier_list)

    def inspect_import_items_for_define_nesting(
        self,
        import_row,
        contained_type_token,
        typename_table,
        imported_module,
        modifier_table,
        error_message,
        types_to_check,
    ):
        for item in import_row.items:
            if item.name_token.literal == contained_type_token.literal:
                type_name_rows = typename_table.get_rows_by_name_and_module(
                    contained_type_token.literal, imported_module.module_id
                )
                if len(type_name_rows) != 1:
                    # return, since duplicates are already caught by the define name collision check
                    return
                type_name_row = type_name_rows[0]
                if self.is_public(type_name_row, modifier_table):
                    self.check_for_invalid_nested_defines(
                        type_name_row,
                        contained_type_token,
                        error_message,
                        types_to_check,
                        True,
                    )

    def check_for_invalid_nested_defines(
        self,
        type_name_row,
        contained_type_token,
        error_message,
        types_to_check,
        skip=False,
    ):
        define_table = self.database.get_table("defines")
        if type_name_row.category in types_to_check["acceptable_user_def_types"]:
            return
        if type_name_row.category == "defined_type":
            if skip:
                return
            nested_define_row = define_table.get_item_by_id(type_name_row.object_id)
            if (
                nested_define_row.built_in_type_token.type_symbol
                in types_to_check["acceptable_define_stmt_types"]
            ):
                return
            else:
                self.add_error(contained_type_token, error_message)
        elif type_name_row.category in (
            "struct",
            "union",
            "enum",
            "interface",
            "error",
        ):
            self.add_error(contained_type_token, error_message)
        else:
            print(f"type name row category not found: {type_name_row.category}")

    def enforce_define_rules(self, undefined_items):
        self.check_that_there_are_no_cycles_in_defined_types(undefined_items)
        self.enforce_nested_define_rules()


class UnionProxy:
    def __init__(self, name_token, item_list):
        self.name_token = name_token
        self.fields = item_list
