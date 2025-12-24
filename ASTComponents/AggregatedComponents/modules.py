from ErrorHandling.semantic_error_messages import (
    DUPLICATE_IMPORT_IN_MODULE,
    MODULE_ITEM_NAME_COLLISION,
    IMPORT_ITEM_NAME_COLLIDES_WITH_MODULE_ITEM,
    IMPORT_ITEM_NAME_COLLISION,
    IMPORT_STATEMENT_HAS_SAME_NAME_AS_ITS_MODULE,
    IMPORT_ITEM_HAS_SAME_NAME_AS_ITS_MODULE,
    IMPORTED_ITEM_NOT_FOUND,
    DUPLICATE_IMPORTED_ITEM,
    STRUCT_FIELD_NAME_COLLIDES_WITH_MODULE_ITEM,
    STRUCT_METHOD_NAME_COLLIDES_WITH_MODULE_ITEM,
    STRUCT_FIELD_NAME_COLLIDES_WITH_IMPORT_ITEM,
    STRUCT_METHOD_NAME_COLLIDES_WITH_IMPORT_ITEM,
)


# After parsing is done, as well as local analysis, a list of these objects
# is what is produced. This is the raw data that is then used to generate
# the IL for autopilot, called APIL.
class RawModule:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.directory_path = None
        self.included_files = []
        self.excluded_files = []
        self.module_statements = []
        self.key_value_defines = []
        self.hash_defines = []
        self.list_defines = []
        self.queue_defines = []
        self.stack_defines = []
        self.option_defines = []
        self.result_defines = []
        self.function_type_defines = []
        self.enums = []
        self.errors = []
        self.interfaces = []
        self.unions = []
        self.structs = []
        self.functions = []
        self.imports = []
        self.unit_tests = []
        self.built_in_libs = dict()
        self.module_collection = None
        self.dependencies = []

    def add_module_dependency(self, module_dependency):
        if str(type(module_dependency).__name__) != "RawModule":
            raise Exception("Not a Raw module!")
        if module_dependency is not None:
            self.dependencies.append(module_dependency)

    def set_module_collection(self, module_collection):
        self.module_collection = module_collection

    def get_module_name_token(self):
        return self.module_statements[0].get_name()

    def get_built_in_libs(self):
        return self.built_in_libs

    def inspect_and_assign_imports(self, error_manager) -> None:
        for import_statement in self.imports:
            imported_module_name_token = import_statement.get_source_name()
            imported_items = import_statement.get_import_list()
            for import_list_item in imported_items:
                import_list_item_name = import_list_item.get_actual_item_name()
                if import_statement.is_library():
                    actual_matching_item_list = self.module_collection.get_library_items_by_library_name_and_item_name(
                        imported_module_name_token, import_list_item_name
                    )
                else:
                    actual_matching_item_list = self.module_collection.get_module_items_by_mod_name_and_item_name(
                        imported_module_name_token, import_list_item_name
                    )
                if len(actual_matching_item_list) < 1:
                    error_manager.add_error(
                        import_list_item_name, IMPORTED_ITEM_NOT_FOUND
                    )
                elif len(actual_matching_item_list) > 1:
                    for actual_item in actual_matching_item_list:
                        error_manager.add_error(
                            import_list_item_name,
                            DUPLICATE_IMPORTED_ITEM,
                            actual_item.get_name(),
                        )
                else:
                    actual_item = actual_matching_item_list[0]
                    import_list_item.set_ref_to_actual_type(actual_item)

    def item_count(self):
        count = len(self.module_statements)
        count += len(self.key_value_defines)
        count += len(self.hash_defines)
        count += len(self.list_defines)
        count += len(self.queue_defines)
        count += len(self.stack_defines)
        count += len(self.option_defines)
        count += len(self.result_defines)
        count += len(self.function_type_defines)
        count += len(self.enums)
        count += len(self.errors)
        count += len(self.interfaces)
        count += len(self.unions)
        count += len(self.structs)
        count += len(self.functions)
        count += len(self.imports)
        count += len(self.unit_tests)
        return count

    def get_module_item_name_tokens(self):
        items = self.get_all_non_import_items()
        return [item.get_name() for item in items]

    def get_all_non_import_items(self):
        items = []
        items.extend([item for item in self.key_value_defines])
        items.extend([item for item in self.hash_defines])
        items.extend([item for item in self.list_defines])
        items.extend([item for item in self.queue_defines])
        items.extend([item for item in self.stack_defines])
        items.extend([item for item in self.option_defines])
        items.extend([item for item in self.result_defines])
        items.extend([item for item in self.function_type_defines])
        items.extend([item for item in self.enums])
        items.extend([item for item in self.errors])
        items.extend([item for item in self.unions])
        items.extend([item for item in self.structs])
        items.extend([item for item in self.functions])
        items.extend([item for item in self.interfaces])
        items.extend([item for item in self.unit_tests])
        return items

    def get_all_imported_item_names(self):
        imported_items = self.get_all_imported_items()
        return [item.get_visible_item_name() for item in imported_items]

    def get_all_imported_items(self):
        import_items = []
        for import_statement in self.imports:
            for import_item in import_statement.get_import_list():
                import_items.append(import_item)
        return import_items

    def get_actual_imported_items_from_other_module(self, module_name, item_name):
        return self.module_collection.get_module_items_by_mod_name_and_item_name(
            module_name, item_name
        )

    def get_matching_items_for_name(self, name):
        items = []
        for item in self.get_all_non_import_items():
            if item.get_name().literal == name.literal:
                items.append(item)
        for import_statement in self.imports:
            for imported_type_name in import_statement.get_import_list():
                if imported_type_name.get_visible_item_name().literal == name.literal:
                    # matching_imported_types.append(imported_type_name)
                    module_name_token = import_statement.get_imported_name_token()
                    actual_item_name = imported_type_name.get_actual_item_name()
                    items.extend(
                        self.get_actual_imported_items_from_other_module(
                            module_name_token, actual_item_name
                        )
                    )
        return items
    
    def all_items_have_types(self) -> bool:
        for item in self.get_all_non_import_items():
            if not item.all_items_have_types():
                return False
        return True


class RawModuleCollection:
    def __init__(self, raw_modules, error_manager):
        self.raw_modules = raw_modules
        for module in self.raw_modules:
            module.set_module_collection(self)
        self.error_manager = error_manager
        self.built_in_libs = dict()

    def get_error_manager(self):
        return self.error_manager

    def has_errors(self):
        return self.error_manager.has_errors(True)

    def report_errors(self):
        self.error_manager.report_errors()

    def get_raw_modules(self):
        return self.raw_modules

    def add_built_in_libs(self, built_in_libs):
        self.built_in_libs.update(built_in_libs)
        for module in self.raw_modules:
            module.built_in_libs.update(built_in_libs)

    def get_built_in_libs(self):
        return self.built_in_libs


    def get_import_items_by_mod_name_and_item_name(self, module_name, item_name):
        items = []
        for module in self.raw_modules:
            if module.get_module_name_token().literal == module_name.literal:
                for item in module.get_all_imported_items():
                    if item.get_visible_item_name().literal == item_name.literal:
                        items.append(item.get_ref_to_actual_item())
                break
        return items

    def get_module_items_by_mod_name_and_item_name(self, module_name, item_name, include_private = False):
        items = []
        for module in self.raw_modules:
            if module.get_module_name_token().literal == module_name.literal:
                for item in module.get_all_non_import_items():
                    if item.get_name().literal == item_name.literal:
                        if item.is_public() or include_private:
                            items.append(item)
                break
        return items

    def get_library_items_by_library_name_and_item_name(self, library_name, item_name):
        if library_name.literal not in self.built_in_libs:
            return []
        library = self.built_in_libs[library_name.literal]
        if library.has_item(item_name.literal):
            return [library.get_item(item_name.literal)]
        else:
            return []


    def check_modules(self) -> None:
        for module in self.get_raw_modules():
            self.check_for_imports_of_same_module(module)
            self.check_name_collisions_amongst_import_statements(module)
            self.check_for_name_collisions_of_types_in_module(module)
            self.check_for_name_collisions_between_module_items_and_import_items(module)
            self.check_for_name_collisions_between_module_and_import(module)

    def check_for_imports_of_same_module(self, module: RawModule) -> None:
        for i in range(len(module.imports)):
            current_import_stmt = module.imports[i]
            current_imported_module_name = current_import_stmt.get_source_name()
            for j in range(i + 1, len(module.imports)):
                other_module = module.imports[j]
                other_imported_module_name = other_module.get_source_name()
                if (
                    current_imported_module_name.literal
                    == other_imported_module_name.literal
                ):
                    self.error_manager.add_error(
                        current_imported_module_name,
                        DUPLICATE_IMPORT_IN_MODULE,
                        other_imported_module_name,
                    )

    def check_name_collisions_amongst_import_statements(
        self, module: RawModule
    ) -> None:
        for i in range(len(module.imports)):
            current_import = module.imports[i]
            for j in range(i + 1, len(module.imports)):
                other_module = module.imports[j]
                for current_import_item in current_import.get_import_list():
                    for other_import_item in other_module.get_import_list():
                        if (
                            current_import_item.get_visible_item_name().literal
                            == other_import_item.get_visible_item_name().literal
                        ):
                            self.error_manager.add_error(
                                current_import_item.get_visible_item_name(),
                                IMPORT_ITEM_NAME_COLLISION,
                                other_import_item.get_visible_item_name(),
                            )

    def check_for_name_collisions_of_types_in_module(self, module: RawModule) -> None:
        all_items = module.get_all_non_import_items()
        for i in range(len(all_items)):
            current_item = all_items[i]
            for j in range(i + 1, len(all_items)):
                other_item = all_items[j]
                if current_item.get_name().literal == other_item.get_name().literal:
                    self.error_manager.add_error(
                        current_item.get_name(),
                        MODULE_ITEM_NAME_COLLISION,
                        other_item.get_name(),
                    )
            if str(type(current_item).__name__) == "StructStatement":
                self._check_struct_internal_items_against_other_module_items(
                    current_item, i, all_items
                )

    def _check_struct_internal_items_against_other_module_items(
        self, struct, struct_index, all_module_items
    ):
        for i in range(len(all_module_items)):
            if i == struct_index:
                continue
            other_item = all_module_items[i]
            self.check_struct_items_against_external_items(
                struct.get_fields(),
                other_item.get_name(),
                STRUCT_FIELD_NAME_COLLIDES_WITH_MODULE_ITEM,
            )
            self.check_struct_items_against_external_items(
                struct.get_functions(),
                other_item.get_name(),
                STRUCT_METHOD_NAME_COLLIDES_WITH_MODULE_ITEM,
            )

    def check_for_name_collisions_between_module_items_and_import_items(
        self, module: RawModule
    ) -> None:
        for item in module.get_all_non_import_items():
            for import_stmt in module.imports:
                for import_item in import_stmt.get_import_list():
                    if (
                        item.get_name().literal
                        == import_item.get_visible_item_name().literal
                    ):
                        self.error_manager.add_error(
                            import_item.get_visible_item_name(),
                            IMPORT_ITEM_NAME_COLLIDES_WITH_MODULE_ITEM,
                            item.get_name(),
                        )
                    if str(type(item).__name__) == "StructStatement":
                        self.check_struct_items_against_external_items(
                            item.get_fields(),
                            import_item.get_visible_item_name(),
                            STRUCT_FIELD_NAME_COLLIDES_WITH_IMPORT_ITEM,
                        )
                        self.check_struct_items_against_external_items(
                            item.get_functions(),
                            import_item.get_visible_item_name(),
                            STRUCT_METHOD_NAME_COLLIDES_WITH_IMPORT_ITEM,
                        )

    def check_struct_items_against_external_items(
        self, current_item_members, other_item_name_token, err_msg
    ):
        for item in current_item_members:
            if item.get_name().literal == other_item_name_token.literal:
                self.error_manager.add_error(
                    item.get_name(), err_msg, other_item_name_token
                )

    def check_for_name_collisions_between_module_and_import(
        self, module: RawModule
    ) -> None:
        for import_stmt in module.imports:
            if import_stmt.get_source_name().literal == module.name:
                self.error_manager.add_error(
                    import_stmt.get_source_name(),
                    IMPORT_STATEMENT_HAS_SAME_NAME_AS_ITS_MODULE,
                    module.get_module_name_token(),
                )
            for import_item in import_stmt.get_import_list():
                if import_item.get_visible_item_name().literal == module.name:
                    self.error_manager.add_error(
                        import_item.get_visible_item_name(),
                        IMPORT_ITEM_HAS_SAME_NAME_AS_ITS_MODULE,
                        module.get_module_name_token(),
                    )

    def check_imports_for_existing_items(self) -> None:
        checked_modules = set()
        unchecked_modules = list()
        for module in self.raw_modules:
            if module.name == "main":
                unchecked_modules.append(module)
                break
        if len(unchecked_modules) == 0:
            raise Exception("Didn't find main module")
        self._check_module_imports_for_item_existence(
            unchecked_modules, checked_modules
        )

    def _check_module_imports_for_item_existence(
        self, unchecked_modules: list[RawModule], checked_modules: set[RawModule]
    ) -> None:
        next_unchecked_modules = list()
        for unchecked_module in unchecked_modules:
            unchecked_module.inspect_and_assign_imports(self.get_error_manager())
            checked_modules.add(unchecked_module)
            for dependency in unchecked_module.dependencies:
                if dependency not in checked_modules:
                    next_unchecked_modules.append(dependency)
        if len(next_unchecked_modules) > 0:
            next_unchecked_modules = [
                module
                for module in next_unchecked_modules
                if module not in checked_modules
            ]
            self._check_module_imports_for_item_existence(
                next_unchecked_modules, checked_modules
            )

    def all_items_have_types(self) -> bool:
        for module in self.raw_modules:
            if not module.all_items_have_types():
                return False
        return True