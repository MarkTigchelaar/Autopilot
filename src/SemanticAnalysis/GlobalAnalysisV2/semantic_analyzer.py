from ErrorHandling.error_manager import ErrorManager
import ErrorHandling.semantic_error_messages as ErrMsg
from ASTComponents.raw_modules import RawModuleCollection
from SemanticAnalysis.GlobalAnalysisV2.import_analyzer import ImportAnalyzer
from SemanticAnalysis.GlobalAnalysisV2.define_analyzer import DefineAnalyzer


class SemanticAnalyzer:
    def __init__(
        self, error_manager: ErrorManager, collected_modules: RawModuleCollection
    ):
        self.error_manager = error_manager
        self.collected_modules = collected_modules
        self.import_analyzer = ImportAnalyzer(
            self.error_manager, self.collected_modules
        )
        self.define_analyzer = DefineAnalyzer(
            self.error_manager, self.collected_modules
        )

    def add_error(self, comparer_token, error_message, comparee_token):
        self.error_manager.add_semantic_error(
            comparer_token, error_message, comparee_token
        )

    def analyze(self):
        self.analyze_modules()
        self.check_for_name_collisions_in_modules()
        self.import_analyzer.analyze()
        self.define_analyzer.analyze()

    def analyze_modules(self):
        modules = self.collected_modules.get_raw_modules()
        for i in range(len(modules)):
            comparer_module = modules[i]
            for j in range(i + 1, len(modules)):
                if i == j:
                    continue
                comparee_module = modules[j]
                if (
                    comparee_module.get_module_name_token().literal
                    == comparer_module.get_module_name_token().literal
                ):
                    self.add_error(
                        comparee_module.get_module_name_token(),
                        ErrMsg.NON_UNIQUE_MODULE,
                        comparer_module.get_module_name_token(),
                    )

            self.check_items_in_module_for_name_collisions_with_module(comparer_module)

    def check_items_in_module_for_name_collisions_with_module(self, raw_module):
        item_name_tokens = raw_module.get_module_item_name_tokens()
        for item_name_token in item_name_tokens:
            if item_name_token.literal == raw_module.get_module_name_token().literal:
                self.add_error(
                    item_name_token,
                    ErrMsg.MODULE_NAME_AND_ITEM_COLLISION,
                    raw_module.get_module_name_token(),
                )

    def check_for_name_collisions_in_modules(self):
        for raw_module in self.collected_modules.get_raw_modules():
            item_name_tokens = raw_module.get_module_item_name_tokens()
            for i in range(len(item_name_tokens)-1):
                for j in range(i + 1, len(item_name_tokens)):
                    if item_name_tokens[i].literal == item_name_tokens[j].literal:
                        self.add_error(
                            item_name_tokens[i],
                            ErrMsg.MODULE_ITEM_NAME_COLLISION,
                            item_name_tokens[j]
                        )