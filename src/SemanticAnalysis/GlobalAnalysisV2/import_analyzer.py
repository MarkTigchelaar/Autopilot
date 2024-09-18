from ErrorHandling.error_manager import ErrorManager
import ErrorHandling.semantic_error_messages as ErrMsg
from ASTComponents.raw_modules import RawModuleCollection
from SemanticAnalysis.AnalysisComponents.module_path_matcher import ModulePathMatcher


class ImportAnalyzer:
    def __init__(
        self, error_manager: ErrorManager, collected_modules: RawModuleCollection
    ):
        self.error_manager = error_manager
        self.collected_modules = collected_modules

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)

    def analyze(self):
        raw_modules = self.collected_modules.get_raw_modules()
        for i, raw_module in enumerate(raw_modules):
            self.analyze_individual_module(i, raw_module, raw_modules)

    def analyze_individual_module(self, index, raw_module, raw_modules):
        for import_index, import_stmt in enumerate(raw_module.imports):
            imported_module_maybe = self.check_imported_module_exists(
                index, import_stmt, raw_module, raw_modules
            )
            if imported_module_maybe is None:
                continue
            first_module_that_matches = imported_module_maybe
            self.check_for_duplicate_imports(raw_module, import_stmt, import_index)
            self.check_for_name_collisions_from_other_imported_modules(
                import_index, import_stmt, raw_module, raw_modules
            )
            self.check_for_name_collisions_with_other_items_in_module(
                index, import_stmt, raw_module
            )
            self.check_for_existence_of_items_being_imported(
                import_stmt, first_module_that_matches
            )

    def check_for_duplicate_imports(self, raw_module, import_stmt, import_index):
        for j, other_import_stmt in enumerate(raw_module.imports):
            if j <= import_index:
                continue
            if (
                other_import_stmt.get_imported_name_token().literal
                == import_stmt.get_imported_name_token().literal
            ):
                self.add_error(
                    other_import_stmt.get_imported_name_token(),
                    ErrMsg.DUPLICATE_IMPORT_IN_MODULE,
                    import_stmt.get_imported_name_token(),
                )

    def check_imported_module_exists(self, index, import_stmt, raw_module, raw_modules):
        if not self.check_module_defined(import_stmt, raw_module, raw_modules):
            return None
        possible_modules = self.get_possible_modules(
            import_stmt, raw_module, raw_modules
        )
        return self.collect_matching_modules(raw_module, possible_modules, import_stmt)

    def get_possible_modules(self, import_stmt, raw_module, raw_modules):
        possible_modules = []
        for other_raw_module in raw_modules:
            if other_raw_module == raw_module:
                continue
            if (
                import_stmt.get_imported_name_token().literal
                == other_raw_module.get_module_name_token().literal
            ):
                possible_modules.append(other_raw_module)
        return possible_modules

    def collect_matching_modules(self, raw_module, possible_modules, import_stmt):
        import_path_to_module = import_stmt.get_path_list()[0:-1]
        module_id = -8888
        path_matcher = ModulePathMatcher(
            module_id,
            import_path_to_module,
            raw_module.directory_path,
            self.error_manager,
        )
        path_matcher.collect_valid_paths()
        modules_that_match = path_matcher.collect_matching_modules(possible_modules)
        imported_module_name = import_stmt.get_imported_name_token()
        if len(modules_that_match) < 1:
            self.add_error(imported_module_name, ErrMsg.INVALID_IMPORTED_MODULE_PATH)
            return None
        elif len(modules_that_match) > 1:
            for mod in modules_that_match:
                # This is a change in behaviour, and causes duplicate errors
                # Will be chalked up to: Dont have so many matching modules
                if mod != raw_module:
                    self.add_error(
                        imported_module_name,
                        ErrMsg.MULTIPLE_MODULES_FOUND_ON_PATH,
                        mod.get_module_name_token(),
                    )
            for mod in modules_that_match:
                if mod != raw_module:
                    return mod
        else:
            return modules_that_match[0]

    def check_module_defined(self, import_stmt, raw_module, raw_modules):
        for other_raw_module in raw_modules:
            if other_raw_module == raw_module:
                continue
            if (
                import_stmt.get_imported_name_token().literal
                == other_raw_module.get_module_name_token().literal
            ):
                return True
        if self.check_for_imported_libraries(import_stmt):
            return True  # No need to do remainder of checks for libraries
        self.add_error(
            import_stmt.get_imported_name_token(), ErrMsg.INVALID_IMPORTED_MODULE
        )
        return False

    def check_for_imported_libraries(self, import_stmt):
        # deal with libraries later
        return False

    def check_for_name_collisions_from_other_imported_modules(
        self, import_index, import_stmt, raw_module, raw_modules
    ):
        # items in import statement cannot duplicate other items in other import statements
        # in same module
        for import_item in import_stmt.get_import_list():
            if import_item.get_visible_item_name().literal == import_stmt.get_imported_name_token().literal:
                self.add_error(
                    import_item.get_visible_item_name(),
                    ErrMsg.IMPORT_ITEM_HAS_SAME_NAME_AS_ITS_MODULE,
                )
            for i, other_import in enumerate(raw_module.imports):
                if i <= import_index:
                    continue
                for other_import_item in other_import.get_import_list():
                    self.check_names_if_no_aliases_used(import_item, other_import_item)
                    self.check_names_if_one_alias_used(import_item, other_import_item)
                    self.check_names_if_two_aliases_used(import_item, other_import_item)

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

    def check_for_name_collisions_with_other_items_in_module(
        self, index, import_stmt, raw_module
    ):
        module_item_names = raw_module.get_module_item_name_tokens()
        for module_item_name in module_item_names:
            for import_item in import_stmt.get_import_list():
                if (
                    module_item_name.literal
                    == import_item.get_visible_item_name().literal
                ):
                    self.add_error(
                        import_item.get_visible_item_name(),
                        ErrMsg.IMPORT_ITEM_NAME_COLLIDES_WITH_MODULE_ITEM,
                        module_item_name,
                    )

    def check_for_existence_of_items_being_imported(
        self, import_stmt, first_module_that_matches
    ):
        items_in_module = first_module_that_matches.get_all_non_import_items()
        for import_item in import_stmt.get_import_list():
            found = False
            for module_item in items_in_module:
                if not module_item.is_public():
                    continue

                if import_item.get_actual_item_name().literal == module_item.get_name().literal:
                    found = True
                    print(f"found item: {import_item.get_actual_item_name()}")
                    break
            if not found:
                self.add_error(
                    import_item.get_visible_item_name(), ErrMsg.IMPORTED_ITEM_NOT_FOUND
                )
