from ASTComponents.AggregatedComponents.modules import RawModuleCollection, RawModule
from ErrorHandling.semantic_error_manager import SemanticErrorManager
from SemanticAnalysis.LocalAnalysis.enum_analysis import analyze_enum
from SemanticAnalysis.LocalAnalysis.error_analysis import analyze_error
from SemanticAnalysis.LocalAnalysis.union_analysis import analyze_union
from SemanticAnalysis.LocalAnalysis.import_analysis import analyze_import
from SemanticAnalysis.LocalAnalysis.define_analysis import analyze_define
from SemanticAnalysis.LocalAnalysis.function_analysis import analyze_function
from SemanticAnalysis.LocalAnalysis.interface_analysis import analyze_interface
from SemanticAnalysis.LocalAnalysis.struct_analysis import analyze_struct


class LocalSemanticAnalyzer:
    def __init__(
        self,
        module_collection: RawModuleCollection,
        error_manager: SemanticErrorManager,
    ):
        self.modules = module_collection.get_raw_modules()
        self.error_manager = error_manager
        self.seen_modules = set()

    def analyze_program(self):
        main_module = self._find_main()
        self._analyze_modules([main_module])

    def _find_main(self) -> RawModule:
        for module in self.modules:
            if module.name == "main":
                return module
        raise Exception("main module not found")

    def _analyze_modules(self, modules: list[RawModule]):
        dependencies = list()
        for module in modules:
            if module in self.seen_modules:
                continue
            self._analyze_module(module)
            self.seen_modules.add(module)
            dependencies.extend(module.dependencies)
        if len(dependencies) > 0:
            self._analyze_modules(dependencies)

    def _analyze_module(self, module: RawModule):
        for module_import in module.imports:
            analyze_import(self.error_manager, module_import)

        for define in module.key_value_defines:
            analyze_define(self.error_manager, define)
        for define in module.linear_type_defines:
            analyze_define(self.error_manager, define)
        for define in module.failable_type_defines:
            analyze_define(self.error_manager, define)
        for define in module.function_type_defines:
            analyze_define(self.error_manager, define)

        for enum in module.enums:
            analyze_enum(self.error_manager, enum)
        for error in module.errors:
            analyze_error(self.error_manager, error)
        for union in module.unions:
            analyze_union(self.error_manager, union)

        for function in module.functions:
            analyze_function(self.error_manager, function)
        for interface in module.interfaces:
            analyze_interface(self.error_manager, interface)
        for struct in module.structs:
            analyze_struct(self.error_manager, struct)
