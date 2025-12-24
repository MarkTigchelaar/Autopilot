from typing import List
from ASTComponents.AggregatedComponents.modules import RawModule, RawModuleCollection

from ErrorHandling.semantic_error_manager import SemanticErrorManager
from ErrorHandling.semantic_error_messages import TYPE_NOT_DEFINED

# from Tokenization.symbols import INT, LONG, FLOAT, DOUBLE, CHAR, STRING, BOOL
import Tokenization.symbols as symbols
from ASTComponents.AggregatedComponents.primitives import (
    PrimitiveType,
    Integer,
    Long,
    Float,
    Double,
    Char,
    String,
    Bool,
    Null,
)

from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.key_value_define import (
    TypeResolvedKVDefine,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.hash_define import (
    TypeResolvedHashDefine,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.list_define import (
    TypeResolvedListDefine,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.queue_define import (
    TypeResolvedQueueDefine,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.stack_define import (
    TypeResolvedStackDefine,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.option_define import (
    TypeResolvedOptionDefine,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.result_define import (
    TypeResolvedResultDefine,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.function_type_define import (
    TypeResolvedFunctionTypeDefine,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.enum import (
    TypeResolvedEnum,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.error import (
    TypeResolvedError,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.interface import (
    TypeResolvedInterface,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.union import (
    TypeResolvedUnion,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.struct import (
    TypeResolvedStruct,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.function import (
    TypeResolvedFunction,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.unittest import (
    TypeResolvedUnitTest,
)


class TypeResolvedModuleCollection:
    def __init__(self, module_collection: RawModuleCollection):
        self.error_manager: SemanticErrorManager = module_collection.get_error_manager()
        self.raw_module_collection: RawModuleCollection = module_collection
        self.resolved_modules: List[TypeResolvedModule] = []
        # Represents the global use of primitive types
        self.integer_ref = Integer()
        self.long_ref = Long()
        self.float_ref = Float()
        self.double_ref = Double()
        self.char_ref = Char()
        self.string_ref = String()
        self.bool_ref = Bool()
        self.null_ref = Null()

    def build_resolved_ast(self) -> None:
        for raw_module in self.raw_module_collection.get_raw_modules():
            self.resolved_modules.append(self._annotate_module(raw_module))

    def _annotate_module(self, raw_module: RawModule):
        resolved_module = TypeResolvedModule(
            raw_module, self.error_manager, self.raw_module_collection, self
        )
        resolved_module.annotate_module_items()
        return resolved_module

    def get_primitive_by_item_type_name(self, name_token):
        return self.get_primitive_by_symbol_type(name_token.internal_type)
    

    def get_primitive_by_symbol_type(self, symbol_type):
        type_instance = None
        match symbol_type:
            case symbols.INT:
                type_instance = self.integer_ref
            case symbols.LONG:
                type_instance = self.long_ref
            case symbols.FLOAT:
                type_instance = self.float_ref
            case symbols.DOUBLE:
                type_instance = self.double_ref
            case symbols.CHAR:
                type_instance = self.char_ref
            case symbols.STRING:
                type_instance = self.string_ref
            case symbols.BOOL:
                type_instance = self.bool_ref
            case symbols.NULL:
                type_instance = self.null_ref
        return type_instance


class TypeResolvedModule:
    def __init__(
        self,
        raw_module: RawModule,
        error_manager: SemanticErrorManager,
        module_collection: RawModuleCollection,
        parent: TypeResolvedModuleCollection,
    ):
        self.raw_module = raw_module
        self.error_manager = error_manager
        self.module_collection = module_collection
        self.parent_module_collection = parent

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
        #self.imports = []
        self.unit_tests = []


    def annotate_module_items(self):
        self.annotate_key_value_defines()
        self.annotate_hash_defines()
        self.annotate_list_defines()
        self.annotate_queue_defines()
        self.annotate_stack_defines()
        self.annotate_option_defines()
        self.annotate_result_defines()
        self.annotate_function_type_defines()
        self.annotate_enums()
        self.annotate_errors()
        self.annotate_interfaces()
        self.annotate_unions()
        self.annotate_structs()
        self.annotate_functions()
        self.annotate_unit_tests()

    def annotate_key_value_defines(self):
        for kv_pair in self.raw_module.key_value_defines:
            typed_kv_pair = TypeResolvedKVDefine(
                kv_pair,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_kv_pair.resolve_types()
            self.key_value_defines.append(typed_kv_pair)

    def annotate_hash_defines(self):
        for hash in self.raw_module.hash_defines:
            typed_hash = TypeResolvedHashDefine(
                hash,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_hash.resolve_types()
            self.hash_defines.append(typed_hash)

    def annotate_list_defines(self):
        for list_define in self.raw_module.list_defines:
            typed_list = TypeResolvedListDefine(
                list_define,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_list.resolve_types()
            self.list_defines.append(typed_list)

    def annotate_queue_defines(self):
        for queue_define in self.raw_module.queue_defines:
            typed_queue = TypeResolvedQueueDefine(
                queue_define,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_queue.resolve_types()
            self.queue_defines.append(typed_queue)

    def annotate_stack_defines(self):
        for stack_define in self.raw_module.stack_defines:
            typed_stack = TypeResolvedStackDefine(
                stack_define,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_stack.resolve_types()
            self.stack_defines.append(typed_stack)

    def annotate_option_defines(self):
        for option_define in self.raw_module.option_defines:
            typed_option = TypeResolvedOptionDefine(
                option_define,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_option.resolve_types()
            self.option_defines.append(typed_option)

    def annotate_result_defines(self):
        for result_define in self.raw_module.result_defines:
            typed_result = TypeResolvedResultDefine(
                result_define,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_result.resolve_types()
            self.result_defines.append(typed_result)

    def annotate_function_type_defines(self):
        for func_type in self.raw_module.function_type_defines:
            typed_func_type = TypeResolvedFunctionTypeDefine(
                func_type,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_func_type.resolve_types()
            self.function_type_defines.append(typed_func_type)

    def annotate_enums(self):
        for enum in self.raw_module.enums:
            typed_enum = TypeResolvedEnum(
                enum,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_enum.resolve_types()
            self.enums.append(typed_enum)

    def annotate_errors(self):
        for error in self.raw_module.errors:
            typed_error = TypeResolvedError(
                error,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_error.resolve_types()
            self.errors.append(typed_error)

    def annotate_interfaces(self):
        for interface in self.raw_module.interfaces:
            typed_interface = TypeResolvedInterface(
                interface,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_interface.resolve_types()
            self.interfaces.append(typed_interface)

    def annotate_unions(self):
        for union in self.raw_module.unions:
            typed_union = TypeResolvedUnion(
                union,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_union.resolve_types()
            self.unions.append(typed_union)

    def annotate_structs(self):
        for struct in self.raw_module.structs:
            typed_struct = TypeResolvedStruct(
                struct,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_struct.resolve_types()
            self.structs.append(typed_struct)

    def annotate_functions(self):
        for function in self.raw_module.functions:
            typed_function = TypeResolvedFunction(
                function,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_function.resolve_types()
            self.functions.append(typed_function)

    def annotate_unit_tests(self):
        for unit_test in self.raw_module.unit_tests:
            typed_unit_test = TypeResolvedUnitTest(
                unit_test,
                self.error_manager,
                self,
                self.parent_module_collection,
            )
            typed_unit_test.resolve_types()
            self.unit_tests.append(typed_unit_test)

    def get_imported_types_by_name(self, name_token):
        return self.module_collection.get_import_items_by_mod_name_and_item_name(
            self.raw_module.get_module_name_token(), name_token
        )

    def get_non_imported_types_by_name(self, name_token):
        return self.module_collection.get_module_items_by_mod_name_and_item_name(
            self.raw_module.get_module_name_token(), name_token, True
        )

    def get_primitive_by_item_type_name(self, name_token):
        return self.parent_module_collection.get_primitive_by_item_type_name(name_token)
    
    def get_primitive_by_symbol_type(self, symbol_type):
        return self.parent_module_collection.get_primitive_by_symbol_type(symbol_type)