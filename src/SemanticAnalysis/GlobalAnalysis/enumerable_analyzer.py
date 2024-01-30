import ErrorHandling.semantic_error_messages as ErrMsg


class EnumerableAnalyzer:
    def __init__(self, database, error_manager):
        self.database = database
        self.error_manager = error_manager

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)

    def analyze(self, object_id):
        (
            enumerable_table,
            typename_table,
            import_table,
            enumerable_row,
            type_row,
            current_module_id,
            name_of_enumerable,
            module_items,
        ) = self.get_tables_and_rows_for_enumerables(object_id)
        if import_table.module_has_imports(current_module_id):
            imports = import_table.get_imports_by_module_id(current_module_id)
        else:
            imports = list()
        self.check_name_collision(type_row, module_items)
        if type_row.category == "union":
            self.check_union_members(enumerable_row, type_row, module_items, imports)

    def get_tables_and_rows_for_enumerables(self, object_id):
        enumerable_table = self.database.get_table("enumerables")
        typename_table = self.database.get_table("typenames")
        import_table = self.database.get_table("imports")
        enumerable_row = enumerable_table.get_item_by_id(object_id)
        type_row = typename_table.get_item_by_id(object_id)
        current_module_id = type_row.module_id
        name_of_enumerable = type_row.name_token
        module_items = typename_table.get_items_by_module_id(current_module_id)
        return (
            enumerable_table,
            typename_table,
            import_table,
            enumerable_row,
            type_row,
            current_module_id,
            name_of_enumerable,
            module_items,
        )

    def check_name_collision(self, type_row, module_items):
        name_of_enumerable = type_row.name_token
        for item in module_items:
            if item.name_token.literal == name_of_enumerable.literal:
                if type_row.object_id >= item.object_id:
                    continue
                self.add_error(
                    name_of_enumerable,
                    ErrMsg.ENUMERABLE_NAME_COLLISION_IN_MODULE,
                    item.name_token,
                )
        # No need to check enum name against import items, since import tests cover this
        # Also don't check names of fields in enumerables, since they are addressed as enum_instance.fieldname

    def check_union_members(self, union_row, type_row, module_items, imports):
        for union_field in union_row.item_list:
            union_field_matched_to_type = False
            for item in module_items:
                if item.object_id == type_row.object_id:
                    continue
                if union_field.type_token.literal == item.name_token.literal:
                    if union_field_matched_to_type:
                        self.add_error(
                            union_field.type_token,
                            ErrMsg.UNION_MEMBER_NAME_ALREADY_MATCHED_TO_TYPE,
                            item.name_token,
                        )
                    union_field_matched_to_type = True
                    if type_row.object_id >= item.object_id:
                        continue
                    if self.type_allowed_in_union(item):
                        continue
                    self.add_error(
                        union_field.type_token,
                        ErrMsg.UNION_MEMBER_INVALID_TYPE,
                        item.name_token,
                    )
            self.check_union_fields_against_imports(
                union_field, type_row, imports, union_field_matched_to_type
            )

    def check_union_fields_against_imports(
        self, union_field, type_row, imports, matched
    ):
        for import_row in imports:
            for import_item in import_row.items:
                if import_item.new_name_token:
                    if (
                        import_item.new_name_token.literal
                        == union_field.type_token.literal
                    ):
                        if matched:
                            self.add_error(
                                union_field.type_token,
                                ErrMsg.UNION_MEMBER_NAME_ALREADY_MATCHED_TO_TYPE,
                                import_item.new_name_token,
                            )
                        matched = True

                        # get module item from imported module
                        # check if it is correct type for union
                        # use imported module name, get module id, then get items in module, match name, check type
                        imported_module_name = import_row.imported_module_name_token
                        other_module_items = self.find_other_module_items(
                            imported_module_name
                        )
                        specific_module_item = self.get_specific_module_item(
                            other_module_items, import_item
                        )
                        if self.type_allowed_in_union(specific_module_item):
                            continue
                        self.add_error(
                            union_field.type_token,
                            ErrMsg.UNION_MEMBER_INVALID_TYPE,
                            specific_module_item.name_token,
                        )

                elif import_item.name_token.literal == union_field.type_token.literal:
                    if matched:
                        self.add_error(
                            union_field.type_token,
                            ErrMsg.UNION_MEMBER_NAME_ALREADY_MATCHED_TO_TYPE,
                            import_item.name_token,
                        )
                    matched = True
                    imported_module_name = import_row.imported_module_name_token
                    other_module_items = self.find_other_module_items(
                        imported_module_name
                    )
                    specific_module_item = self.get_specific_module_item(
                        other_module_items, import_item
                    )
                    if self.type_allowed_in_union(specific_module_item):
                        continue
                    self.add_error(
                        union_field.type_token,
                        ErrMsg.UNION_MEMBER_INVALID_TYPE,
                        specific_module_item.name_token,
                    )

    def type_allowed_in_union(self, item):
        # We check the type defined in the module, since the union itself does not know what type it is
        if item.category == "struct":
            return True
        if item.category == "enum":
            return False
        if item.category == "union":
            return False
        if item.category == "error":
            return False
        if item.category == "interface":
            return True
        if item.category == "defined_type":
            return True
        if item.category == "fn_header":
            return False
        # type can be primitives, but no need to check for that, since this is a module item,
        # primitives do not show up as module items
        raise Exception(
            "INTERNAL ERROR: Invalid category for union member: {}".format(
                item.category
            )
        )

    def find_other_module_items(self, imported_module_name):
        module_table = self.database.get_table("modules")
        typename_table = self.database.get_table("typenames")
        if module_table.is_module_defined(imported_module_name.literal):
            module_rows = module_table.get_modules_data_for_name(
                imported_module_name.literal
            )
        else:
            raise Exception(
                "INTERNAL ERROR: Module not found: {}".format(imported_module_name)
            )
        module_row = module_rows[0]
        other_module_items = typename_table.get_items_by_module_id(module_row.module_id)
        return other_module_items

    def get_specific_module_item(self, other_module_items, import_item):
        for item in other_module_items:
            if item.name_token.literal == import_item.name_token.literal:
                return item
        raise Exception(
            "INTERNAL ERROR: Item not found in module: {}".format(
                import_item.name_token.literal
            )
        )
