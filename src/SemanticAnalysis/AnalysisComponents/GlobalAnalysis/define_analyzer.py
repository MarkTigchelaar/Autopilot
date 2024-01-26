import ErrorHandling.semantic_error_messages as ErrMsg
from keywords import is_primitive_type
from symbols import OPTION, RESULT, MAP, HASHMAP, DICTIONARY, SET, HASHSET, TREESET
import symbols


class DefineAnalyzer:
    def __init__(self, database, error_manager):
        self.database = database
        self.error_manager = error_manager

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)

    def analyze(self, object_id):
        # Check that the definition is not using the same name as some other item in the module.
        # Check that there is no other definition of same name somewhere in the module.
        # Check that the definition is not using the same name as some import item.
        self.check_for_new_typename_collisions(object_id)
        # Check that there is no other definition with the same exact components in the module
        self.check_other_defines_for_same_components(object_id)
        self.check_if_is_function_type_with_no_args_no_return_type(object_id)
        # Check that components of item being defined are also defined.
        undefined_items = self.check_items_in_definition_are_defined(object_id)

        self.enforce_define_rules(object_id, undefined_items)

    def get_tables_and_items(self, object_id):
        import_table = self.database.get_table("imports")
        typename_table = self.database.get_table("typenames")
        define_table = self.database.get_table("defines")
        define_row = define_table.get_item_by_id(object_id)
        current_module_id = define_row.current_module_id
        module_items = typename_table.get_items_by_module_id(current_module_id)
        if import_table.module_has_imports(current_module_id):
            current_module_imports = import_table.get_imports_by_module_id(
                current_module_id
            )
        else:
            current_module_imports = []
        return module_items, define_row, current_module_imports

    def check_module_item(self, module_item, define_row):
        if module_item.object_id <= define_row.object_id:
            return
        if module_item.name_token.literal == define_row.new_type_name_token.literal:
            self.add_error(
                define_row.new_type_name_token,
                ErrMsg.DEFINE_NEW_NAME_COLLISION,
                module_item.name_token,
            )

    def check_import_item(self, item, define_row):
        if item.new_name_token and (
            item.new_name_token.literal == define_row.new_type_name_token.literal
        ):
            self.add_error(
                define_row.new_type_name_token,
                ErrMsg.DEFINE_NEW_NAME_COLLISION_W_IMPORT,
                item.new_name_token,
            )
        elif not item.new_name_token and (
            item.name_token.literal == define_row.new_type_name_token.literal
        ):
            self.add_error(
                define_row.new_type_name_token,
                ErrMsg.DEFINE_NEW_NAME_COLLISION_W_IMPORT,
                item.name_token,
            )

    def check_for_new_typename_collisions(self, object_id):
        module_items, define_row, current_module_imports = self.get_tables_and_items(
            object_id
        )
        for module_item in module_items:
            self.check_module_item(module_item, define_row)
        for import_row in current_module_imports:
            for item in import_row.items:
                self.check_import_item(item, define_row)

    def get_define_table_and_rows(self, object_id):
        define_table = self.database.get_table("defines")
        define_row = define_table.get_item_by_id(object_id)
        current_module_id = define_row.current_module_id
        other_defines = define_table.get_items_by_module_id(current_module_id)
        return define_row, other_defines

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

    def check_other_defines_for_same_components(self, object_id):
        define_row, other_defines = self.get_define_table_and_rows(object_id)
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

    def check_if_is_function_type_with_no_args_no_return_type(self, object_id):
        define_table = self.database.get_table("defines")
        define_row = define_table.get_item_by_id(object_id)
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

    def get_tables_and_rows_for_define_checks(self, object_id):
        import_table = self.database.get_table("imports")
        typename_table = self.database.get_table("typenames")
        define_table = self.database.get_table("defines")
        define_row = define_table.get_item_by_id(object_id)
        current_module_id = define_row.current_module_id
        return import_table, typename_table, define_row, current_module_id

    def get_items_to_check(self, define_row):
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

    def check_items_in_same_module(self, items_to_check, module_items, define_row):
        for i in reversed(range(len(items_to_check))):
            if len(items_to_check) < 1:
                return
            defined_item = items_to_check[i]
            for module_item in module_items:
                if module_item.object_id == define_row.object_id:
                    continue
                if module_item.name_token.literal == defined_item.literal:
                    items_to_check.pop(i)

    def check_items_in_imports(self, items_to_check, imports):
        for i in reversed(range(len(items_to_check))):
            if len(items_to_check) < 1:
                return
            defined_item = items_to_check[i]
            for import_row in imports:
                for imported_item in import_row.items:
                    if len(items_to_check) < 1:
                        return
                    if imported_item.new_name_token:
                        if imported_item.new_name_token.literal == defined_item.literal:
                            items_to_check.pop(i)
                    elif imported_item.name_token:
                        if imported_item.name_token.literal == defined_item.literal:
                            items_to_check.pop(i)

    def check_items_in_definition_are_defined(self, object_id):
        (
            import_table,
            typename_table,
            define_row,
            current_module_id,
        ) = self.get_tables_and_rows_for_define_checks(object_id)
        items_to_check = self.get_items_to_check(define_row)
        if len(items_to_check) < 1:
            return items_to_check
        module_items = typename_table.get_items_by_module_id(current_module_id)
        self.check_items_in_same_module(items_to_check, module_items, define_row)
        if len(items_to_check) < 1:
            return items_to_check
        if import_table.module_has_imports(current_module_id):
            imports = import_table.get_imports_by_module_id(current_module_id)
            self.check_items_in_imports(items_to_check, imports)
        for undefined_item_token in items_to_check:
            self.add_error(undefined_item_token, ErrMsg.UNDEFINED_ITEM_IN_DEFINE_STMT)

        return items_to_check

    def is_not_primitive_or_none(self, token):
        if token is None:
            return False
        return not is_primitive_type(token)

    def check_that_there_are_no_cycles_in_defined_types(
        self, object_id, undefined_items
    ):
        define_table = self.database.get_table("defines")
        define_row = define_table.get_item_by_id(object_id)
        current_module_id = define_row.current_module_id
        struct_table = self.database.get_table("structs")

        if struct_table.is_module_id_defined(current_module_id):
            structs = struct_table.get_items_by_module_id(current_module_id)
        else:
            structs = list()
        if define_table.is_module_id_defined(current_module_id):
            defines = define_table.get_items_by_module_id(current_module_id)
        else:
            defines = list()
        unions = self.get_all_unions_in_module(object_id, current_module_id)
        enums = self.get_all_enum_in_module(object_id, current_module_id)
        errors = self.get_all_errors_in_module(object_id, current_module_id)

        checker = DefineStatementDependencyChecker(
            undefined_items, structs, unions, enums, errors, defines, self.error_manager
        )
        checker.check_dag(define_row)

    def get_all_unions_in_module(self, object_id, current_module_id):
        return self.get_all_enums_in_module(object_id, current_module_id, "union")

    def get_all_enum_in_module(self, object_id, current_module_id):
        return self.get_all_enums_in_module(object_id, current_module_id, "enum")

    def get_all_errors_in_module(self, object_id, current_module_id):
        return self.get_all_enums_in_module(object_id, current_module_id, "error")

    def get_all_enums_in_module(self, object_id, current_module_id, type_name):
        typename_table = self.database.get_table("typenames")
        enumerable_table = self.database.get_table("enumerables")
        enumerables = list()
        for typename in typename_table.get_items_by_module_id(current_module_id):
            if typename.object_id == object_id:
                continue
            if not enumerable_table.is_object_defined(typename.object_id):
                continue
            if typename.category == type_name:
                enumerable = enumerable_table.get_item_by_id(typename.object_id)
                union_proxy = HackyUnionProxy(typename.name_token, enumerable.item_list)
                enumerables.append(union_proxy)
        return enumerables

    def enforce_nested_define_rules(self, object_id):
        define_table = self.database.get_table("defines")
        define_row = define_table.get_item_by_id(object_id)
        # current_module_id = define_row.current_module_id

        # defines = define_table.get_items_by_module_id(current_module_id)

        match define_row.built_in_type_token.type_symbol:
            case symbols.LIST:
                self.analyze_define_elements_for_list_types(define_row)
            case symbols.LINKEDLIST:
                self.analyze_define_elements_for_linked_list_types(define_row)
            case symbols.VECTOR:
                self.analyze_define_elements_for_vector_types(define_row)
            case symbols.MAP:
                self.analyze_define_elements_for_map_types(define_row)
            case symbols.HASHMAP:
                self.analyze_define_elements_for_hashmap_types(define_row)
            case symbols.DICTIONARY:
                self.analyze_define_elements_for_dictionary_types(define_row)
            case symbols.SET:
                self.analyze_define_elements_for_set_types(define_row)
            case symbols.HASHSET:
                self.analyze_define_elements_for_hashset_types(define_row)
            case symbols.TREESET:
                self.analyze_define_elements_for_treeset_types(define_row)
            case symbols.OPTION:
                self.analyze_define_elements_for_option_types(define_row)
            case symbols.RESULT:
                self.analyze_define_elements_for_result_types(define_row)
            case symbols.QUEUE:
                self.analyze_define_elements_for_queue_types(define_row)
            case symbols.FIFOQUEUE:
                self.analyze_define_elements_for_fifo_queue_types(define_row)
            case symbols.DEQUE:
                self.analyze_define_elements_for_deque_types(define_row)
            case symbols.PRIORITYQUEUE:
                self.analyze_define_elements_for_priority_queue_types(define_row)
            case symbols.STACK:
                self.analyze_define_elements_for_stack_types(define_row)
            case symbols.FUN:
                self.analyze_define_elements_for_function_types(define_row)
            case _:
                raise Exception(
                    f"INTERNAL ERROR: Invalid define type found: {define_row.built_in_type_token.type_symbol}"
                )

    def analyze_define_elements_for_map_types(self, define_row):
        # for the values in kv pair:
        self.analyze_define_elements_for_linear_collection_types_default(
            define_row, ErrMsg.MAP_TYPE_VALUE_DEFINE_NESTING_INVALID_DEFINES
        )

        # for keys in kv pair:
        self.analyze_define_elements_for_hash_key_collection_types(
            define_row, ErrMsg.MAP_TYPE_KEY_DEFINE_NESTING_INVALID_DEFINES
        )

    def analyze_define_elements_for_hashmap_types(self, define_row):
        self.analyze_define_elements_for_linear_collection_types_default(
            define_row, ErrMsg.HASHMAP_TYPE_DEFINE_NESTING_INVALID_DEFINES
        )

        self.analyze_define_elements_for_hash_key_collection_types(
            define_row, ErrMsg.HASHMAP_TYPE_KEY_DEFINE_NESTING_INVALID_DEFINES
        )

    def analyze_define_elements_for_dictionary_types(self, define_row):
        self.analyze_define_elements_for_linear_collection_types_default(
            define_row, ErrMsg.DICT_TYPE_DEFINE_NESTING_INVALID_DEFINES
        )

        self.analyze_define_elements_for_hash_key_collection_types(
            define_row, ErrMsg.DICT_TYPE_KEY_DEFINE_NESTING_INVALID_DEFINES
        )

    def analyze_define_elements_for_set_types(self, define_row):
        self.analyze_define_elements_for_hash_collection_types(
            define_row, ErrMsg.SET_TYPE_DEFINE_NESTING_INVALID_DEFINES
        )

    def analyze_define_elements_for_hashset_types(self, define_row):
        self.analyze_define_elements_for_hash_collection_types(
            define_row, ErrMsg.HASHSET_TYPE_DEFINE_NESTING_INVALID_DEFINES
        )

    def analyze_define_elements_for_treeset_types(self, define_row):
        self.analyze_define_elements_for_hash_collection_types(
            define_row, ErrMsg.TREESET_TYPE_DEFINE_NESTING_INVALID_DEFINES
        )

    def analyze_define_elements_for_list_types(self, define_row):
        self.analyze_define_elements_for_linear_collection_types_default(
            define_row, ErrMsg.LIST_TYPE_DEFINE_NESTING_INVALID_DEFINES
        )

    def analyze_define_elements_for_linked_list_types(self, define_row):
        self.analyze_define_elements_for_linear_collection_types_default(
            define_row, ErrMsg.LINKED_LIST_TYPE_DEFINE_NESTING_INVALID_DEFINES
        )

    def analyze_define_elements_for_vector_types(self, define_row):
        self.analyze_define_elements_for_linear_collection_types_default(
            define_row, ErrMsg.VECTOR_TYPE_DEFINE_NESTING_INVALID_DEFINES
        )

    def analyze_define_elements_for_queue_types(self, define_row):
        self.analyze_define_elements_for_linear_collection_types_default(
            define_row, ErrMsg.QUEUE_TYPE_DEFINE_NESTING_INVALID_DEFINES
        )

    def analyze_define_elements_for_fifo_queue_types(self, define_row):
        self.analyze_define_elements_for_linear_collection_types_default(
            define_row, ErrMsg.FIFO_QUEUE_TYPE_DEFINE_NESTING_INVALID_DEFINES
        )

    def analyze_define_elements_for_deque_types(self, define_row):
        self.analyze_define_elements_for_linear_collection_types_default(
            define_row, ErrMsg.DEQUE_TYPE_DEFINE_NESTING_INVALID_DEFINES
        )

    def analyze_define_elements_for_priority_queue_types(self, define_row):
        self.analyze_define_elements_for_linear_collection_types_default(
            define_row, ErrMsg.PRIORITY_QUEUE_TYPE_DEFINE_NESTING_INVALID_DEFINES
        )

    def analyze_define_elements_for_stack_types(self, define_row):
        self.analyze_define_elements_for_linear_collection_types_default(
            define_row, ErrMsg.STACK_TYPE_DEFINE_NESTING_INVALID_DEFINES
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
        # define_table = self.database.get_table("defines")
        typename_table = self.database.get_table("typenames")
        import_table = self.database.get_table("imports")
        module_table = self.database.get_table("modules")
        modifier_table = self.database.get_table("modifiers")
        # contained_type_token = define_row.value_type
        if contained_type_token is None:
            raise Exception("INTERNAL ERROR: contained type token is None")
        if is_primitive_type(contained_type_token):
            return
        if typename_table.is_name_defined_in_module(
            contained_type_token.literal, current_module_id
        ):
            # items_to_check = self.get_items_to_check(define_row)
            type_name_rows = typename_table.get_rows_by_name_and_module(
                contained_type_token.literal, current_module_id
            )
            # for type_name_row in type_name_rows:

            if len(type_name_rows) != 1:
                # Or just return, since duplicates are already caught by the define name collision check
                print("type name rows does not have length 1, skipping")
                return
                # raise Exception("INTERNAL ERROR: Length of type name rows should be 1")
            type_name_row = type_name_rows[0]
            self.check_for_invalid_nested_defines(
                type_name_row, contained_type_token, error_message, types_to_check
            )
        # Revisit making defines public in the future, for now just have defines limited to the module they are defined in

        elif import_table.module_has_imports(current_module_id):
            imports = import_table.get_imports_by_module_id(current_module_id)
            for import_row in imports:
                is_module_defined = module_table.is_module_defined(import_row.imported_module_name_token.literal)
                possible_modules = module_table.get_modules_data_for_name(
                    import_row.imported_module_name_token.literal
                )
                print(f"possible modules: {possible_modules}, is module defined: {is_module_defined}")
                if len(possible_modules) != 1:
                    print("duplicate modules detected, skipping")
                    continue
                    # Is a duplicate, in that case, skip these checks
                    # or, import refers to non existant module, in which case, skip these checks
                imported_module = possible_modules[0]

                for item in import_row.items:
                    if item.name_token.literal == contained_type_token.literal:
                        # check type in module being imported
                        # if len(typename_table.get_rows_by_name_and_module(
                        #     item.name_token,
                        # )) < 1:
                        #     raise Exception(
                        #         "INTERNAL ERROR: Type not found in module being imported"
                        #     )
                        print(f"checking for invalid nested defines: {item.name_token.literal} {item.name_token}")
                        type_name_rows = (
                            typename_table.get_rows_by_name_and_module(
                                contained_type_token.literal, imported_module.module_id
                            )
                        )
                        if len(type_name_rows) != 1:
                            # Or just return, since duplicates are already caught by the define name collision check
                            print("type name rows does not have length 1, skipping")
                            return
                            # raise Exception("INTERNAL ERROR: Length of type name rows should be 1")
                        type_name_row = type_name_rows[0]
                        # Check if it's public, if not, skip it, previous existance check should have caught it
                        if not modifier_table.is_object_defined(type_name_row.object_id):
                            continue
                        modifier_list = modifier_table.get_modifier_list_by_id(
                            type_name_row.object_id
                        )
                        found = False
                        if modifier_list:  # Things like module statements don't have modifiers
                            for mod in modifier_list:
                                if mod.literal == "pub":
                                    found = True
                                    break
                        if not found:
                            # This is an error, but "undefined" types due to them being private 
                            # is already handled
                            continue
                        self.check_for_invalid_nested_defines(
                            type_name_row,
                            contained_type_token,
                            error_message,
                            types_to_check,
                            True
                        )
        else:
            print(
                f"Type not found in module being imported or in home module: {contained_type_token}"
            )

    def check_for_invalid_nested_defines(
        self, type_name_row, contained_type_token, error_message, types_to_check, skip = False
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
        elif type_name_row.category in ("struct", "union", "enum", "interface", "error"):
            self.add_error(contained_type_token, error_message)
        else:
            print(f"type name row category not found: {type_name_row.category}")

    # def check_result_types_are_error_types(self, object_id):
    #     define_table = self.database.get_table("defines")
    #     define_row = define_table.get_item_by_id(object_id)
    #     current_module_id = define_row.current_module_id
    #     typename_table = self.database.get_table("typenames")
    #     enumerable_table = self.database.get_table("enumerables")
    #     if define_row.result_type is None:
    #         return
    #     for typename in typename_table.get_items_by_module_id(current_module_id):
    #         if typename.object_id == object_id:
    #             continue
    #         if not enumerable_table.is_object_defined(typename.object_id):
    #             if typename.name_token.literal == define_row.result_type.literal:
    #                 self.add_error(
    #                     define_row.result_type,
    #                     ErrMsg.NON_ERROR_TYPE_IN_RESULT,
    #                     typename.name_token,
    #                 )
    #                 return
    #             else:
    #                 continue
    #         if typename.category == "error":
    #             if typename.name_token.literal == define_row.result_type.literal:
    #                 return
    #     # Types should be defined by this point, if one is still not, explode:
    #     raise Exception("INTERNAL ERROR: Type not found")

    def check_types_are_hashable_for_maps_and_sets(self, object_id):
        define_table = self.database.get_table("defines")
        define_row = define_table.get_item_by_id(object_id)
        current_module_id = define_row.current_module_id
        typename_table = self.database.get_table("typenames")
        import_table = self.database.get_table("imports")

        if define_row.built_in_type_token.type_symbol not in (
            MAP,
            HASHMAP,
            DICTIONARY,
            SET,
            HASHSET,
            TREESET,
        ):
            return
        for typename in typename_table.get_items_by_module_id(current_module_id):
            if typename.object_id == object_id:
                continue
            # if not typename_table.is_object_defined(typename.object_id):
            #     continue
            if define_row.built_in_type_token.type_symbol in (MAP, HASHMAP, DICTIONARY):
                if typename.name_token.literal == define_row.key_type.literal:
                    self.check_for_hashable_methods(typename)
            elif define_row.built_in_type_token.type_symbol in (SET, HASHSET, TREESET):
                if typename.name_token.literal == define_row.value_type.literal:
                    self.check_for_hashable_methods(typename)
        # Also do this for types that are imported into the module
        if import_table.module_has_imports(current_module_id):
            imports = import_table.get_imports_by_module_id(current_module_id)
            for import_row in imports:
                for item in import_row.items:
                    if item.name_token.literal == define_row.key_type.literal:
                        # check type in module being imported
                        if not typename_table.is_object_defined(
                            item.name_token.object_id
                        ):
                            raise Exception(
                                "INTERNAL ERROR: Type not found in module being imported"
                            )
                        typename = typename_table.get_item_by_id(
                            item.name_token.object_id
                        )
                        self.check_for_hashable_methods(typename)
                    if item.name_token.literal == define_row.value_type.literal:
                        # check type in module being imported
                        if not typename_table.is_object_defined(
                            item.name_token.object_id
                        ):
                            raise Exception(
                                "INTERNAL ERROR: Type not found in module being imported"
                            )
                        typename = typename_table.get_item_by_id(
                            item.name_token.object_id
                        )
                        self.check_for_hashable_methods(typename)

    def check_for_hashable_methods(self, typename):
        object_id = typename.object_id

        match typename.category:
            case "union":
                enumerable_table = self.database.get_table("enumerables")
                union_row = enumerable_table.get_item_by_id(object_id)
                if union_row.name_token.literal == typename.name_token.literal:
                    self.add_error(
                        union_row.name_token.literal, ErrMsg.UNIONS_NOT_HASHABLE
                    )
                    return
                else:
                    raise Exception(
                        "INTERNAL ERROR: Union not found in check_for_hashable_methods"
                    )
            case "defined_type":
                raise Exception(
                    "INTERNAL ERROR: Defined type found in check_for_hashable_methods"
                )
            case "error":
                enumerable_table = self.database.get_table("enumerables")
                error_row = enumerable_table.get_item_by_id(object_id)
                if error_row.name_token.literal == typename.name_token.literal:
                    self.add_error(
                        error_row.name_token.literal, ErrMsg.ERRORS_NOT_HASHABLE
                    )
                    return
                else:
                    raise Exception(
                        "INTERNAL ERROR: Error not found in check_for_hashable_methods"
                    )
            case "struct":
                struct_table = self.database.get_table("structs")
                struct_row = struct_table.get_item_by_id(object_id)
                functions = struct_row.functions
                hash_function = None
                # eq_function = None
                for function in functions:
                    if function.header.name_token.literal == "hash":
                        hash_function = function
                    # if function.header.name_token.literal == "equals":
                    #     eq_function = function
                if hash_function is None:
                    # self.add_error(struct_row.name_token.literal, ErrMsg.STRUCT_MISSING_HASH_FUNCTION)
                    # structs should be hashable by defualt by using their memory address
                    return
                else:
                    if hash_function.header.return_type.literal != "int":
                        self.add_error(
                            struct_row.name_token.literal,
                            ErrMsg.STRUCT_HASH_FUNCTION_WRONG_RETURN_TYPE,
                        )
                    if len(hash_function.header.arg_list) != 0:
                        self.add_error(
                            struct_row.name_token.literal,
                            ErrMsg.STRUCT_HASH_FUNCTION_WRONG_ARG_COUNT,
                        )
                    return

            case "interface":
                self.add_error(
                    typename.name_token.literal, ErrMsg.INTERFACES_NOT_HASHABLE
                )
                return  # interfaces can be hashable ... later ... maybe
            case "enum":
                enumerable_table = self.database.get_table("enumerables")
                enum_row = enumerable_table.get_item_by_id(object_id)
                if enum_row.name_token.literal == typename.name_token.literal:
                    self.add_error(
                        enum_row.name_token.literal, ErrMsg.ENUMS_NOT_HASHABLE
                    )
                    return
                else:
                    raise Exception(
                        "INTERNAL ERROR: Enum not found in check_for_hashable_methods"
                    )
            case "function":
                function_table = self.database.get_table("functions")
                function_row = function_table.get_item_by_id(object_id)
                if (
                    function_row.header.name_token.literal
                    == typename.name_token.literal
                ):
                    self.add_error(
                        function_row.header.name_token.literal,
                        ErrMsg.FUNCTIONS_NOT_HASHABLE,
                    )
                return  # functions are not hashable
            case "primitive":
                return  # primitives are hashable
            case "fn_header":
                raise Exception(
                    "INTERNAL ERROR: Function header found in check_for_hashable_methods"
                )
            case "unittest":
                raise Exception(
                    "INTERNAL ERROR: Unittest found in check_for_hashable_methods"
                )
            case "module_name":
                raise Exception(
                    "INTERNAL ERROR: Module name found in check_for_hashable_methods"
                )
            case _:
                raise Exception(
                    "INTERNAL ERROR: Type not found in check_for_hashable_methods"
                )

    # def check_types_are_sortable_for_lists(self, object_id):
    #     define_table = self.database.get_table("defines")
    #     define_row = define_table.get_item_by_id(object_id)
    #     current_module_id = define_row.current_module_id
    #     typename_table = self.database.get_table("typenames")

    #     if define_row.built_in_type_token.type_symbol not in (LIST, LINKEDLIST, VECTOR):
    #         return
    #     for typename in typename_table.get_items_by_module_id(current_module_id):
    #         if typename.object_id == object_id:
    #             continue
    #         if typename.name_token.literal == define_row.value_type.literal:
    #             self.check_for_comparable_methods(typename)

    # def check_for_comparable_methods(self, typename):
    #     pass

    def enforce_define_rules(self, object_id, undefined_items):
        self.check_that_there_are_no_cycles_in_defined_types(object_id, undefined_items)

        # TODO
        # a result in a option cannot be an option
        # a option in a result cannot be a result
        # self.check_for_invalid_option_and_result_type_relationships(object_id)

        self.enforce_nested_define_rules(object_id)
        return

        # nested define rules cover this already
        # self.check_result_types_are_error_types(object_id)
        # self.check_types_are_hashable_for_maps_and_sets(object_id)

        # self.check_types_are_sortable_for_lists(object_id) <- this check should be done if a sort() is present on the collection
        # uses compare method
        # re use check_types_are_hashable_for_maps_and_sets, send args in, and check for compare method


# Just one more sign that a major refactor is needed. This is a hacky way to get around the fact that
# the union type stores its name in the typenames table, which breaks apart the union type into its
# components. This is a hacky way to get around that.
# The typename table should just be used as a reference. The union type name should also be stored in its own table.
class HackyUnionProxy:
    def __init__(self, name_token, item_list):
        self.name_token = name_token
        self.fields = item_list


class DefineStatementDependencyChecker:
    def __init__(
        self, undefined_items, structs, unions, enums, errors, defines, error_manager
    ):
        self.undefined_items = undefined_items
        self.structs = structs
        self.unions = unions
        self.enums = enums
        self.errors = errors
        self.defines = defines
        self.error_manager = error_manager

        self.visited = set()
        # self.stack = list()
        # self.is_dag = True
        self.defined_type = None

    def check_dag(self, define_row):
        self.defined_type = define_row.new_type_name_token
        self.visited.add(define_row.new_type_name_token.literal)
        self.visit_define(define_row)

    def find_type(self, type):
        for undefined_item in self.undefined_items:
            if type.literal == undefined_item.literal:
                # print(f"found undefined item: {undefined_item.literal} {undefined_item.file_name} {undefined_item.line_number}")
                return
            # else:
            # print(f"not found undefined item: {undefined_item.literal} {undefined_item.file_name} {undefined_item.line_number}")

        for struct_row in self.structs:
            if type.literal == struct_row.name_token.literal:
                self.visit_item_with_fields(struct_row)
                return

        for union_row in self.unions:
            if type.literal == union_row.name_token.literal:
                self.visit_item_with_fields(union_row)
                return

        for enum_row in self.enums:
            if type.literal == enum_row.name_token.literal:
                return

        for error_row in self.errors:
            if type.literal == error_row.name_token.literal:
                return

        for define_row in self.defines:
            if type.literal == define_row.new_type_name_token.literal:
                self.visit_define(define_row)
                return
        print("Type not found in current module, is an imported item")
        # raise Exception(f"INTERNAL ERROR: Type not found: {type.literal} {type.file_name} {type.line_number}")

    def visit_item_with_fields(self, struct_row):
        for field in struct_row.fields:
            if is_primitive_type(field.type_token):
                continue
            if field.type_token.literal in self.visited:
                if field.type_token.literal == self.defined_type.literal:
                    self.error_manager.add_semantic_error(
                        self.defined_type,
                        ErrMsg.CYCLE_IN_DEFINE_DEPENDANCIES,
                        field.type_token,
                    )
            else:
                self.visited.add(field.type_token.literal)
                self.find_type(field.type_token)

    def visit_define(self, define_row):
        key_type = define_row.key_type
        value_type = define_row.value_type
        arg_list = define_row.arg_list
        result_type = define_row.result_type

        if key_type and not is_primitive_type(key_type):
            self.find_type(key_type)

        if value_type and not is_primitive_type(value_type):
            self.find_type(value_type)

        if result_type and not is_primitive_type(result_type):
            self.find_type(result_type)

        if arg_list is None:
            return
        for arg in arg_list:
            if arg and not is_primitive_type(arg):
                self.find_type(arg)
