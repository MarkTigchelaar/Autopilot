import ErrorHandling.semantic_error_messages as ErrMsg
from keywords import is_primitive_type


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
        self.check_items_in_definition_are_defined(object_id)

    def get_tables_and_items(self, object_id):
        import_table = self.database.get_table("imports")
        typename_table = self.database.get_table("typenames")
        define_table = self.database.get_table("defines")
        define_row = define_table.get_item_by_id(object_id)
        current_module_id = define_row.current_module_id
        module_items = typename_table.get_items_by_module_id(current_module_id)
        current_module_imports = import_table.get_imports_by_module_id(
            current_module_id
        )
        return module_items, define_row, current_module_imports

    def check_module_item(self, module_item, define_row):
        if module_item.object_id == define_row.object_id:
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
                ErrMsg.DEFINE_NEW_NAME_COLLISION,
                item.new_name_token,
            )
        elif item.name_token.literal == define_row.new_type_name_token.literal:
            self.add_error(
                define_row.type_name_token,
                ErrMsg.DEFINE_NEW_NAME_COLLISION,
                item.new_name_token,
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
                    self.add_error(
                        define_row.built_in_type_token,
                        ErrMsg.DEFINE_USES_SAME_COMPONENTS,
                        other_define.built_in_type_token,
                    )

    def check_value_type(self, define_row, other_define):
        if (define_row.value_type and other_define.value_type) and not (
            define_row.union_type or other_define.union_type
        ):
            if not (define_row.arg_list or other_define.arg_list):
                if define_row.value_type.literal == other_define.value_type.literal:
                    self.add_error(
                        define_row.built_in_type_token,
                        ErrMsg.DEFINE_USES_SAME_COMPONENTS,
                        other_define.built_in_type_token,
                    )

    def check_union_type(self, define_row, other_define):
        if (define_row.value_type and other_define.value_type) and (
            define_row.union_type and other_define.union_type
        ):
            if define_row.value_type.literal == other_define.value_type.literal:
                if define_row.union_type == other_define.union_type:
                    if define_row.union_type.literal == other_define.union_type.literal:
                        self.add_error(
                            define_row.union_type,
                            ErrMsg.DEFINE_USES_SAME_COMPONENTS,
                            other_define.union_type,
                        )

    def check_function_signature(self, define_row, other_define):
        if define_row.arg_list and other_define.arg_list:
            if len(define_row.arg_list) == len(other_define.arg_list):
                arg_literals = [arg.literal for arg in define_row.arg_list]
                other_arg_literals = [arg.literal for arg in define_row.arg_list]
                arg_literals.sort()
                other_arg_literals.sort()
                same = all(a == b for a, b in zip(arg_literals, other_arg_literals))
                if same and (define_row.value_type and other_define.value_type):
                    if define_row.value_type.literal == other_define.value_type.literal:
                        self.add_error(
                            define_row.built_in_type_token,
                            ErrMsg.DEFINE_USES_SAME_COMPONENTS,
                            other_define.built_in_type_token,
                        )
                elif same:
                    self.add_error(
                        define_row.built_in_type_token,
                        ErrMsg.DEFINE_USES_SAME_COMPONENTS,
                        other_define.built_in_type_token,
                    )

    def check_other_defines_for_same_components(self, object_id):
        define_row, other_defines = self.get_define_table_and_rows(object_id)
        for other_define in other_defines:
            if define_row.object_id == other_define.object_id:
                continue
            if (
                define_row.built_in_type_token.literal
                != other_define.built_in_type_token.literal
            ):
                continue
            self.check_key_type(define_row, other_define)
            self.check_value_type(define_row, other_define)
            self.check_union_type(define_row, other_define)
            self.check_function_signature(define_row, other_define)

    def check_if_is_function_type_with_no_args_no_return_type(self, object_id):
        define_table = self.database.get_table("defines")
        define_row = define_table.get_item_by_id(object_id)
        if define_row.key_type:
            return
        if define_row.value_type:
            return
        # not needed, but add just in case
        if define_row.union_type:
            return
        if define_row.arg_list and len(define_row.arg_list) > 0:
            return
        self.add_error(
            define_row.built_in_type_token, ErrMsg.FUNCTION_TYPE_HAS_NO_EFFECT
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
            define_row.union_type,
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
            return
        module_items = typename_table.get_items_by_module_id(current_module_id)
        self.check_items_in_same_module(items_to_check, module_items, define_row)
        if len(items_to_check) < 1:
            return
        imports = import_table.get_imports_by_module_id(current_module_id)
        self.check_items_in_imports(items_to_check, imports)
        for undefined_item_token in items_to_check:
            self.add_error(undefined_item_token, ErrMsg.UNDEFINED_ITEM_IN_DEFINE_STMT)

    def is_not_primitive_or_none(self, token):
        if token is None:
            return False
        return not is_primitive_type(token)
