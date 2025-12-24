from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode
from Tokenization.symbols import NULL


class TypeResolvedHeader(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, type_annontated_module, parent):
        super().__init__(raw_node, error_manager, type_annontated_module, parent)
        self.argument_type_refs = []

    def resolve_types(self):
        for argument in self.raw_node.get_args():
            type_token = argument.get_type()
            actual_type = self._attempt_type_instance_aqqusition(type_token)
            if actual_type:
                self.argument_type_refs.append(actual_type)
            else:
                self.argument_type_refs.append(None)
                self._add_type_error(type_token)
        return_type = self.raw_node.get_return_type()
        if return_type:
            actual_type = self._attempt_type_instance_aqqusition(return_type)
            if actual_type:
                self._set_verified_type_reference(actual_type)
            else:
                self._add_type_error(return_type)
        else:
            null_type = self.type_annontated_module.get_primitive_by_symbol_type(NULL)
            self._set_verified_type_reference(null_type)
