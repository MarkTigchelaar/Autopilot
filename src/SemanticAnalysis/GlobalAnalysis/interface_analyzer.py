import ErrorHandling.semantic_error_messages as ErrMsg


class InterfaceAnalyzer:
    def __init__(self, database, error_manager):
        self.database = database
        self.error_manager = error_manager

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)

    def analyze(self, object_id):
        (
            typename_table,
            import_table,
            interface_table,
            fn_header_table,
        ) = self.get_tables()
        header_list = self.get_header_list(interface_table, fn_header_table, object_id)
        module_items, current_module_id, name_of_interface = self.get_module_items(
            typename_table, object_id
        )

        self.check_name_collisions(module_items, header_list, name_of_interface)
        self.check_import_collisions(
            import_table, header_list, current_module_id, name_of_interface
        )
        self.check_arg_types(typename_table, header_list, current_module_id)

    def get_tables(self):
        typename_table = self.database.get_table("typenames")
        import_table = self.database.get_table("imports")
        interface_table = self.database.get_table("interfaces")
        fn_header_table = self.database.get_table("fn_headers")
        return typename_table, import_table, interface_table, fn_header_table

    def get_header_list(self, interface_table, fn_header_table, object_id):
        header_id_list = interface_table.get_item_by_id(object_id)
        header_list = [
            fn_header_table.get_item_by_id(header_id) for header_id in header_id_list
        ]
        return header_list

    def get_module_items(self, typename_table, object_id):
        type_row = typename_table.get_item_by_id(object_id)
        current_module_id = type_row.module_id
        name_of_interface = type_row.name_token
        module_items = typename_table.get_items_by_module_id(current_module_id)
        return module_items, current_module_id, name_of_interface

    def check_name_collisions(self, module_items, header_list, name_of_interface):
        for module_item in module_items:
            if module_item.name_token.literal == name_of_interface.name_token.literal:
                self.add_error(
                    name_of_interface.name_token,
                    ErrMsg.INTERFACE_NAME_COLLIDES_WITH_MODULE_ITEM,
                    module_item.name_token,
                )
            self.check_header_collisions(header_list, module_item)

    def check_header_collisions(self, header_list, module_item):
        for header in header_list:
            name_token = header.get_name()
            if name_token.literal == module_item.name_token.literal:
                self.add_error(
                    name_token,
                    ErrMsg.INTERFACE_FN_NAME_COLLIDES_WITH_MODULE_ITEM,
                    module_item.name_token,
                )
            self.check_arg_collisions(header, module_item)

    def check_arg_collisions(self, header, module_item):
        for arg in header.get_args():
            if arg.get_name().literal == module_item.name_token.literal:
                self.add_error(
                    arg.get_name(),
                    ErrMsg.INTERFACE_FN_ARG_COLLIDES_WITH_MODULE_ITEM,
                    module_item.name_token,
                )

    def check_import_collisions(
        self, import_table, header_list, current_module_id, name_of_interface
    ):
        imports = import_table.get_imports_by_module_id(current_module_id)
        for import_row in imports:
            for import_item in import_row.items:
                name_token = (
                    import_item.new_name_token
                    if import_item.new_name_token
                    else import_item.name_token
                )
                if name_token.literal == name_of_interface.name_token.literal:
                    self.add_error(
                        name_of_interface.name_token,
                        ErrMsg.INTERFACE_NAME_COLLIDES_WITH_MODULE_ITEM,
                        name_token,
                    )
                self.check_import_header_collisions(header_list, name_token)

    def check_import_header_collisions(self, header_list, name_token):
        for header in header_list:
            header_name_token = header.get_name()
            if header_name_token.literal == name_token.literal:
                self.add_error(
                    header_name_token,
                    ErrMsg.INTERFACE_FN_NAME_COLLIDES_WITH_IMPORT_ITEM,
                    name_token,
                )
            self.check_import_arg_collisions(header, name_token)

    def check_import_arg_collisions(self, header, name_token):
        for arg in header.get_args():
            if arg.get_name().literal == name_token.literal:
                self.add_error(
                    arg.get_name(),
                    ErrMsg.INTERFACE_FN_ARG_COLLIDES_WITH_IMPORT_ITEM,
                    name_token,
                )

    def check_arg_types(self, typename_table, header_list, current_module_id):
        ok_arg_types = ["interfaces", "structs", "defines", "enums", "unions"]
        forbidden_types = ["functions", "errors"]
        for header in header_list:
            for arg in header.get_args():
                arg_type_token = arg.get_type()
                found = False
                module_items = typename_table.get_items_by_module_id(current_module_id)
                found = self.check_module_item_types(
                    module_items, arg_type_token, ok_arg_types, forbidden_types, found
                )
                if not found:
                    self.check_imported_types_for_arg(arg_type_token, current_module_id)

    def check_module_item_types(
        self, module_items, arg_type_token, ok_arg_types, forbidden_types, found
    ):
        for module_item in module_items:
            item_object_id = module_item.object_id
            try:
                table_name = self.database.get_tablename_for_object(item_object_id)
            except:
                self.add_error(arg_type_token, ErrMsg.UNDEFINED_TYPE)
            if table_name in forbidden_types:
                self.add_error(arg_type_token, ErrMsg.INVALID_FUNCTION_ARG_TYPE)
            elif table_name in ok_arg_types:
                if module_item.name_token.literal == arg_type_token.literal:
                    found = True
                    break
            else:
                raise Exception(
                    "INTERNAL ERROR: type checking encountered a unknown error"
                )
        return found
