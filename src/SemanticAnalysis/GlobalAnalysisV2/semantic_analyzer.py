from ErrorHandling.error_manager import ErrorManager
import ErrorHandling.semantic_error_messages as ErrMsg
from ASTComponents.raw_modules import RawModuleCollection
from SemanticAnalysis.GlobalAnalysisV2.import_analyzer import ImportAnalyzer

class SemanticAnalyzer:
    def __init__(self, error_manager: ErrorManager, collected_modules: RawModuleCollection):
        self.error_manager = error_manager
        self.collected_modules = collected_modules
        self.import_analyzer = ImportAnalyzer(self.error_manager, self.collected_modules)

    def add_error(self, comparer_token, error_message, comparee_token):
        self.error_manager.add_semantic_error(comparer_token, error_message, comparee_token)
    
    
    def analyze(self):
        self.analyze_modules()
        self.import_analyzer.analyze()

    

    def analyze_modules(self):
        modules = self.collected_modules.get_raw_modules()
        for i in range(len(modules)):
            comparer_module = modules[i]
            for j in range(i + 1, len(modules)):
                if i == j:
                    continue
                comparee_module = modules[j]
                if comparee_module.get_module_name_token().literal == comparer_module.get_module_name_token().literal:
                    self.add_error(
                        comparee_module.get_module_name_token(),
                        ErrMsg.NON_UNIQUE_MODULE,
                        comparer_module.get_module_name_token()
                    )
