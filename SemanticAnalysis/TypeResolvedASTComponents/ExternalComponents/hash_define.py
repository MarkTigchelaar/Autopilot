from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedDefine


class TypeResolvedHashDefine(TypeResolvedDefine):
    def resolve_types(self):
        key_type_token = self.raw_node.get_value_token()
        actual_type = self._attempt_type_instance_aqqusition(key_type_token)
        if actual_type:
            self._set_verified_raw_type_reference(actual_type)
        else:
            self._add_type_error(key_type_token)