from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode



class TypeResolvedKVDefine(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, type_annontated_module, parent):
        super().__init__(raw_node, error_manager, type_annontated_module, parent)
        self.value_type_ref = None

    def resolve_types(self):
        key_type_token = self.raw_node.get_key_token()
        value_type_token = self.raw_node.get_value_token()
        actual_type = self._attempt_type_instance_aqqusition(key_type_token)
        if actual_type:
            self._set_verified_type_reference(actual_type)
        else:
            self._add_type_error(key_type_token)
        actual_type = self._attempt_type_instance_aqqusition(value_type_token)
        if actual_type:
            self.value_type_ref = actual_type
        else:
            self._add_type_error(value_type_token)