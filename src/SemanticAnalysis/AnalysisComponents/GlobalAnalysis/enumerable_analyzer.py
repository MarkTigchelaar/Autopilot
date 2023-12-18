import ErrorHandling.semantic_error_messages as ErrMsg


class EnumerableAnalyzer:
    def __init__(self, database, error_manager):
        self.database = database
        self.error_manager = error_manager

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)

    def analyze(self, object_id):
        (
            import_table,
            enumerable_row,
            type_row,
            current_module_id,
            name_of_enumerable,
            module_items,
        ) = self.get_tables_and_rows_for_enumerables(object_id)
        items_to_check = self.check_name_collision(name_of_enumerable, module_items)
        for item in module_items:
            for enumerable_item in enumerable_row.item_list:
                # This code demonstrates that stuffing these types in the same table was a mistake
                match type_row.category:
                    case "enum" | "error":
                        self.check_enumerable_item(
                            enumerable_item,
                            item,
                            type_row,
                            current_module_id,
                            import_table,
                        )
                    case "union":
                        self.check_union_item(enumerable_item, item, items_to_check)
                    case _:
                        raise Exception(
                            f"INTERNAL ERROR: type row category invalid: {type_row.category}"
                        )

        imports = import_table.get_imports_by_module_id(current_module_id)
        self.check_imported_items(items_to_check, imports)

        for union_member in items_to_check:
            self.add_error(union_member.type_token, ErrMsg.UNDEFINED_ITEM_IN_UNION_STMT)

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

    def check_name_collision(self, name_of_enumerable, module_items):
        items_to_check = list()
        for item in module_items:
            if item.name_token.literal == name_of_enumerable.literal:
                self.add_error(
                    name_of_enumerable.literal,
                    ErrMsg.ENUMERABLE_NAME_COLLISION_IN_MODULE,
                    item.name_token,
                )
            return items_to_check

    def check_enumerable_item(
        self, enumerable_item, item, type_row, current_module_id, import_table
    ):
        if enumerable_item.item_name_token.literal == item.name_token.literal:
            self.add_error(
                enumerable_item.item_name_token,
                ErrMsg.ENUMERABLE_LIST_ITEM_NAME_COLLISION_IN_MODULE,
                item.name_token,
            )
        imports = import_table.get_imports_by_module_id(current_module_id)
        self.check_imported_items_against_fieldnames(imports, enumerable_item)

    def check_union_item(self, enumerable_item, item, items_to_check):
        if enumerable_item.item_name_token.literal == item.name_token.literal:
            self.add_error(
                enumerable_item.item_name_token,
                ErrMsg.ENUMERABLE_LIST_ITEM_NAME_COLLISION_IN_MODULE,
                item.name_token,
            )
        if (
            enumerable_item in items_to_check
            and enumerable_item.type_token.literal == item.name_token.literal
        ):
            items_to_check.remove(enumerable_item)
        elif enumerable_item not in items_to_check:
            items_to_check.append(enumerable_item)

    def check_imported_items(self, items_to_check, imports):
        for i in reversed(range(len(items_to_check))):
            for import_row in imports:
                for imported_item in import_row.items:
                    if len(items_to_check) < 1:
                        return
                    if imported_item.new_name_token:
                        if (
                            imported_item.new_name_token.literal
                            == items_to_check[i].type_token.literal
                        ):
                            items_to_check.pop(i)
                    elif imported_item.name_token:
                        if (
                            imported_item.name_token.literal
                            == items_to_check[i].type_token.literal
                        ):
                            items_to_check.pop(i)

    def check_imported_items_against_fieldnames(self, imports, enumerable_item):
        for import_stmt in imports:
            for import_item in import_stmt.items:
                if import_item.new_name_token:
                    if (
                        import_item.new_name_token.literal
                        == enumerable_item.item_name_token.literal
                    ):
                        self.add_error(
                            enumerable_item.item_name_token,
                            ErrMsg.ENUMERABLE_LIST_ITEM_NAME_COLLISION_IN_IMPORT,
                            import_item.new_name_token,
                        )
                elif (
                    import_item.name_token.literal
                    == enumerable_item.item_name_token.literal
                ):
                    self.add_error(
                        enumerable_item.item_name_token,
                        ErrMsg.ENUMERABLE_LIST_ITEM_NAME_COLLISION_IN_IMPORT,
                        import_item.new_name_token,
                    )
