import ErrorHandling.semantic_error_messages as ErrMsg
from SemanticAnalysis.AnalysisComponents.module_path_matcher import ModulePathMatcher
from SemanticAnalysis.Database.Queries.import_items_in_module_query import ImportItemsInModuleQuery
from SemanticAnalysis.Database.Queries.single_import_query import SingleImportQuery

class ImportAnalyzer:
    def __init__(self, database, error_manager, import_dependency_graph):
        self.database = database
        self.error_manager = error_manager
        self.import_dependency_graph = import_dependency_graph

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)

    def analyze(self, object_id):
        imported_module_id = self.check_imported_module_exists(object_id)
        if imported_module_id is None:
            return
        self.add_imported_module_to_dependency_graph(imported_module_id, object_id)
        self.check_for_duplicated_imports(object_id)
        self.check_for_name_collisions_from_other_imported_modules(object_id)
        self.check_for_name_collisions_with_other_items_in_module(object_id)
        self.check_for_existence_of_items_being_imported(object_id, imported_module_id)

    def get_imported_data(self, object_id):
        import_table = self.database.get_table("imports")
        file_table = self.database.get_table("files")
        module_table = self.database.get_table("modules")

        imported_data = import_table.get_row_by_id(object_id)
        imported_module_name = imported_data.imported_module_name
        imported_module_token = imported_data.path[-1].node_token
        return (
            imported_data,
            imported_module_name,
            imported_module_token,
            file_table,
            module_table,
        )

    def check_module_defined(
        self, imported_module_name, imported_module_token, module_table
    ):
        if not module_table.is_module_defined(imported_module_name):
            self.add_error(imported_module_token, ErrMsg.INVALID_IMPORTED_MODULE)
            return False
        return True

    def check_file_defined(self, imported_data, file_table):
        import_stmt_file_name = imported_data.filename
        module_id = imported_data.current_module_id
        if not file_table.is_file_defined(module_id, import_stmt_file_name):
            raise Exception("INTERNAL ERROR: File for import statement not found")
        return module_id

    def get_path_matcher(self, imported_data, module_id, module_table):
        module_data = module_table.get_module_for_id(module_id)
        import_path_to_module = imported_data.path[0:-1]  # don't include module itself
        path_matcher = ModulePathMatcher(
            module_id, import_path_to_module, module_data.path, self.error_manager
        )
        return path_matcher

    def check_imported_module_exists(self, object_id):
        (
            imported_data,
            imported_module_name,
            imported_module_token,
            file_table,
            module_table,
        ) = self.get_imported_data(object_id)
        if not self.check_module_defined(
            imported_module_name, imported_module_token, module_table
        ):
            return None
        possible_modules = module_table.get_modules_data_for_name(imported_module_name)
        module_id = self.check_file_defined(imported_data, file_table)
        path_matcher = self.get_path_matcher(imported_data, module_id, module_table)
        path_matcher.collect_valid_paths()
        modules_that_match = path_matcher.collect_matching_module_ids(possible_modules)
        if len(modules_that_match) < 1:
            self.add_error(imported_module_token, ErrMsg.INVALID_IMPORTED_MODULE_PATH)
        elif len(modules_that_match) > 1:
            for mod_id in modules_that_match:
                if mod_id > module_id:
                    module_row = module_table.get_module_for_id(mod_id)
                    self.add_error(
                        imported_module_token,
                        ErrMsg.MULTIPLE_MODULES_FOUND_ON_PATH,
                        module_row.module_name,
                    )
            return modules_that_match[0]
        else:
            return modules_that_match[0]

    def add_imported_module_to_dependency_graph(self, imported_module_id, object_id):
        import_table = self.database.get_table("imports")
        import_row = import_table.get_row_by_id(object_id)
        current_module_id = import_row.current_module_id
        if object_id not in self.import_dependency_graph:
            self.import_dependency_graph[current_module_id] = list()
        self.import_dependency_graph[current_module_id].append(imported_module_id)

    def get_imports_in_module(self, object_id):
        import_table = self.database.get_table("imports")
        import_row = import_table.get_row_by_id(object_id)
        current_module_id = import_row.current_module_id
        
        return import_table.get_imports_by_module_id(current_module_id), import_row

    def get_matching_imports(self, other_imports_in_module, import_row):
        max_id = -1
        other_matching_imports = list()
        for row in other_imports_in_module:
            if row.imported_module_name == import_row.imported_module_name:
                if row.id == import_row.id:  # only keep other imports
                    continue
                other_matching_imports.append(row)
                if row.id == max_id:
                    raise Exception("INTERNAL ERROR: import row is same id as max_id")
                if row.id > max_id:
                    max_id = row.id
        return other_matching_imports, max_id

    def check_for_duplicated_imports(self, object_id):
        other_imports_in_module, import_row = self.get_imports_in_module(object_id)
        # other_imports_in_module = self.database.execute_query(ImportItemsInModuleQuery(object_id))
        # import_row = self.database.execute_query(SingleImportQuery(object_id)).next()
        other_matching_imports, max_id = self.get_matching_imports(
            other_imports_in_module, import_row
        )

        if max_id >= import_row.id:
            return
        for other_import in other_matching_imports:
            self.add_error(
                import_row.path[-1].node_token,
                ErrMsg.DUPLICATE_IMPORT_IN_MODULE,
                other_import.path[-1].node_token,
            )

    def check_for_name_collisions_from_other_imported_modules(self, object_id):
        import_table = self.database.get_table("imports")
        import_row = import_table.get_row_by_id(object_id)
        current_module_id = import_row.current_module_id
        other_imports_in_module = import_table.get_imports_by_module_id(
            current_module_id
        )
        for current_import_item in import_row.items:
            if current_import_item.new_name_token:
                if (
                    current_import_item.new_name_token.literal
                    == import_row.imported_module_name
                ):
                    self.add_error(
                        current_import_item.new_name_token,
                        ErrMsg.IMPORT_ITEM_HAS_SAME_NAME_AS_ITS_MODULE,
                    )
            else:
                if (
                    current_import_item.name_token.literal
                    == import_row.imported_module_name
                ):
                    self.add_error(
                        current_import_item.name_token,
                        ErrMsg.IMPORT_ITEM_HAS_SAME_NAME_AS_ITS_MODULE,
                    )
            for row in other_imports_in_module:
                # Objects with lower ids, will signify checks already been done.
                if row.id <= object_id:
                    continue
                for other_import_item in row.items:
                    # no error if alias is used, and does not conflict
                    self.check_names_if_no_aliases_used(
                        current_import_item, other_import_item
                    )
                    self.check_names_if_one_alias_used(
                        current_import_item, other_import_item
                    )
                    self.check_names_if_two_aliases_used(
                        current_import_item, other_import_item
                    )

    def check_names_if_no_aliases_used(self, current_import_item, other_import_item):
        if current_import_item.new_name_token or other_import_item.new_name_token:
            return
        if (
            current_import_item.name_token.literal
            == other_import_item.name_token.literal
        ):
            self.add_error(
                current_import_item.name_token,
                ErrMsg.IMPORT_ITEM_NAME_COLLISION,
                other_import_item.name_token,
            )

    def check_names_if_one_alias_used(self, current_import_item, other_import_item):
        if current_import_item.new_name_token and other_import_item.new_name_token:
            return
        if (
            current_import_item.new_name_token is None
            and other_import_item.new_name_token is None
        ):
            return
        if current_import_item.new_name_token and not other_import_item.new_name_token:
            if (
                current_import_item.new_name_token.literal
                == other_import_item.name_token.literal
            ):
                self.add_error(
                    current_import_item.new_name_token,
                    ErrMsg.IMPORT_ITEM_NAME_COLLISION,
                    other_import_item.name_token,
                )
        elif (
            not current_import_item.new_name_token and other_import_item.new_name_token
        ):
            if (
                current_import_item.name_token.literal
                == other_import_item.new_name_token.literal
            ):
                self.add_error(
                    current_import_item.name_token,
                    ErrMsg.IMPORT_ITEM_NAME_COLLISION,
                    other_import_item.new_name_token,
                )

    def check_names_if_two_aliases_used(self, current_import_item, other_import_item):
        if not (
            current_import_item.new_name_token and other_import_item.new_name_token
        ):
            return
        if (
            current_import_item.new_name_token.literal
            == other_import_item.new_name_token.literal
        ):
            self.add_error(
                current_import_item.new_name_token,
                ErrMsg.IMPORT_ITEM_NAME_COLLISION,
                other_import_item.new_name_token,
            )

    def get_module_items(self, object_id):
        import_table = self.database.get_table("imports")
        typename_table = self.database.get_table("typenames")

        import_row = import_table.get_row_by_id(object_id)
        current_module_id = import_row.current_module_id
        return typename_table.get_items_by_module_id(current_module_id), import_row

    def check_for_name_collisions_with_other_items_in_module(self, object_id):
        module_items, import_row = self.get_module_items(object_id)
        for module_item in module_items:
            for imported_item in import_row.items:
                self.check_imported_item(imported_item, module_item)

    def check_imported_item(self, imported_item, module_item):
        if imported_item.new_name_token and (
            imported_item.new_name_token.literal == module_item.name_token.literal
        ):
            self.add_error(
                imported_item.new_name_token,
                ErrMsg.IMPORT_ITEM_NAME_COLLIDES_WITH_MODULE_ITEM,
                module_item.name_token,
            )
        elif (
            not imported_item.new_name_token
            and imported_item.name_token
            and (imported_item.name_token.literal == module_item.name_token.literal)
        ):
            self.add_error(
                imported_item.name_token,
                ErrMsg.IMPORT_ITEM_NAME_COLLIDES_WITH_MODULE_ITEM,
                module_item.name_token,
            )
        elif not imported_item.name_token:
            raise Exception("INTERNAL ERROR: import item has no name")

    def get_tables_and_items_for_import_existence_check(
        self, current_import_id, imported_module_id
    ):
        typename_table = self.database.get_table("typenames")
        import_table = self.database.get_table("imports")
        modifier_table = self.database.get_table("modifiers")
        imported_module_items = typename_table.get_items_by_module_id(
            imported_module_id
        )
        import_row = import_table.get_row_by_id(current_import_id)
        return (
            modifier_table,
            imported_module_items,
            import_row,
        )

    def check_import_item_for_import_existence_check(
        self, import_item, imported_module_item, modifier_table
    ):
        found = False
        if import_item.name_token and (
            import_item.name_token.literal == imported_module_item.name_token.literal
        ):
            if not modifier_table.is_object_defined(imported_module_item.object_id):
                return False
            modifier_list = modifier_table.get_modifier_list_by_id(
                imported_module_item.object_id
            )
            if modifier_list:  # Things like module statements don't have modifiers
                for mod in modifier_list:
                    if mod.literal == "pub":
                        found = True
                        break
        return found

    def check_for_existence_of_items_being_imported(
        self, current_import_id, imported_module_id
    ):
        (
            modifier_table,
            imported_module_items,
            import_row,
        ) = self.get_tables_and_items_for_import_existence_check(
            current_import_id, imported_module_id
        )

        for import_item in import_row.items:
            for imported_module_item in imported_module_items:
                found = False
                found = self.check_import_item_for_import_existence_check(
                    import_item, imported_module_item, modifier_table
                )
                if found:
                    break
            if not found and import_item.name_token:
                self.add_error(import_item.name_token, ErrMsg.IMPORTED_ITEM_NOT_FOUND)
