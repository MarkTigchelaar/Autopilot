from ErrorHandling.error_manager import ErrorManager
import ErrorHandling.semantic_error_messages as ErrMsg
from ASTComponents.raw_modules import RawModuleCollection
from SemanticAnalysis.AnalysisComponents.module_path_matcher import ModulePathMatcher


class DefineAnalyzer:
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
            pass