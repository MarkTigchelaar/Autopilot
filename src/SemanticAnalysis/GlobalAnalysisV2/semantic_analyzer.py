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

            self.check_items_in_module_for_name_collisions_with_module(comparer_module)
    

    def check_items_in_module_for_name_collisions_with_module(self, raw_module):
        self.check_define_statements(raw_module.key_value_defines, raw_module)
        self.check_define_statements(raw_module.linear_type_defines, raw_module)
        self.check_define_statements(raw_module.failable_type_defines, raw_module)
        self.check_define_statements(raw_module.function_type_defines, raw_module)
        self.check_union_statements(raw_module.enums, raw_module)
        self.check_interfaces(raw_module.interfaces, raw_module)
        self.check_structs(raw_module.structs, raw_module)
        self.check_functions(raw_module.functions, raw_module)
        self.check_unittests(raw_module.unit_tests, raw_module)

    def check_define_statements(self, define_stmts, raw_module):
        for define in define_stmts:
            if define.get_descriptor_token().literal == raw_module.get_module_name_token().literal:
                self.add_error(
                    define.get_descriptor_token(),
                    ErrMsg.MODULE_NAME_AND_ITEM_COLLISION,
                    raw_module.get_module_name_token(),
                )
        
    def check_union_statements(self, union_stmts, raw_module):
        for union in union_stmts:
            if union.get_name().literal == raw_module.get_module_name_token().literal:
                self.add_error(
                    union.get_name(),
                    ErrMsg.MODULE_NAME_AND_ITEM_COLLISION,
                    raw_module.get_module_name_token(),
                )
    
    def check_interfaces(self, interfaces, raw_module):
        for interface in interfaces:
            if interface.get_name().literal  == raw_module.get_module_name_token().literal:
                self.add_error(
                    interface.get_name().literal,
                    ErrMsg.MODULE_NAME_AND_ITEM_COLLISION,
                    raw_module.get_module_name_token(),
                )
    
    def check_structs(self, structs, raw_module):
        for struct in structs:
            if struct.get_name().literal  == raw_module.get_module_name_token().literal:
                self.add_error(
                    struct.get_name().literal,
                    ErrMsg.MODULE_NAME_AND_ITEM_COLLISION,
                    raw_module.get_module_name_token(),
                )
    
    def check_functions(self, functions, raw_module):
        for function in functions:
            if function.get_name_token().literal  == raw_module.get_module_name_token().literal:
                self.add_error(
                    function.get_name_token().literal,
                    ErrMsg.MODULE_NAME_AND_ITEM_COLLISION,
                    raw_module.get_module_name_token(),
                )
    
    def check_unittests(self, unit_tests, raw_module):
        for unit_test in unit_tests:
            if unit_test.get_name_token().literal  == raw_module.get_module_name_token().literal:
                self.add_error(
                    unit_test.get_name_token().literal,
                    ErrMsg.MODULE_NAME_AND_ITEM_COLLISION,
                    raw_module.get_module_name_token(),
                )