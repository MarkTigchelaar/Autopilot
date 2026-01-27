from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import (
    TypeResolvedDefine,
)
from Tokenization.symbols import NULL


class TypeResolvedOptionDefine(TypeResolvedDefine):
    def __init__(self, raw_node, error_manager, type_resolved_module, parent):
        super().__init__(raw_node, error_manager, type_resolved_module, parent)
        self.null_type = type_resolved_module.get_primitive_by_symbol_type(NULL)

    def resolve_types(self):
        value_type_token = self.raw_node.get_value_token()
        actual_type = self._attempt_type_instance_aqqusition(value_type_token)
        if actual_type:
            self._set_verified_raw_type_reference(actual_type)
        else:
            self._add_type_error(value_type_token)
