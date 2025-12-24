from ErrorHandling.semantic_error_manager import SemanticErrorManager
import ErrorHandling.semantic_error_messages as ErrMsg
from ASTComponents.AggregatedComponents.modules import RawModuleCollection
from FileSystem.module_path_matcher import ModulePathMatcher


def check_imports(
    error_manager: SemanticErrorManager, collected_modules: RawModuleCollection
):
    analyzer = ImportAnalyzer(error_manager, collected_modules)
    analyzer.analyze()


class ImportAnalyzer:
    def __init__(
        self,
        error_manager: SemanticErrorManager,
        collected_modules: RawModuleCollection,
    ):
        self.error_manager = error_manager
        self.collected_modules = collected_modules

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_error(token, message, shadowed_token)

    def analyze(self):
        raw_modules = self.collected_modules.get_raw_modules()
        for i, raw_module in enumerate(raw_modules):
            self.analyze_individual_module(i, raw_module, raw_modules)

    def analyze_individual_module(self, index, raw_module, raw_modules):
        for import_stmt in raw_module.imports:
            self.check_imported_module_exists(
                index, import_stmt, raw_module, raw_modules
            )

    def check_imported_module_exists(self, index, import_stmt, raw_module, raw_modules):
        if not self.check_module_defined(import_stmt, raw_module, raw_modules):
            return 
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
        import_path_to_module = import_stmt.get_path_list()
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

    def check_module_defined(self, import_stmt, raw_module, raw_modules):
        for other_raw_module in raw_modules:
            if other_raw_module == raw_module:
                continue
            if (
                import_stmt.get_imported_name_token().literal
                == other_raw_module.get_module_name_token().literal
            ):
                return True
        if import_stmt.is_library():
            return False  # No need to do remainder of checks for libraries
        self.add_error(
            import_stmt.get_imported_name_token(), ErrMsg.INVALID_IMPORTED_MODULE
        )
        return False
