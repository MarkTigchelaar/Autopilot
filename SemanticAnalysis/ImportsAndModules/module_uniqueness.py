from ErrorHandling.semantic_error_manager import SemanticErrorManager
import ErrorHandling.semantic_error_messages as ErrMsg
from ASTComponents.AggregatedComponents.modules import RawModuleCollection


def check_for_module_uniqueness(error_manager: SemanticErrorManager, collected_modules: RawModuleCollection):
    modules = collected_modules.get_raw_modules()
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
                error_manager.add_error(
                    comparee_module.get_module_name_token(),
                    ErrMsg.NON_UNIQUE_MODULE,
                    comparer_module.get_module_name_token(),
                )
