from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedDefine


class TypeResolvedFunctionTypeDefine(TypeResolvedDefine):

    def __init__(self, raw_node, error_manager, type_resolved_module, parent):
        super().__init__(raw_node, error_manager, type_resolved_module, parent)
        self.arg_type_refs = []

    def resolve_types(self):
        arg_type_token_list = self.raw_node.get_arg_list()
        return_type_token = self.raw_node.get_return_type()
        actual_return_type = self._attempt_type_instance_aqqusition(return_type_token)
        if actual_return_type:
            self._set_verified_raw_type_reference(actual_return_type)
        else:
            self._add_type_error(return_type_token)

        for arg_token in arg_type_token_list:
            actual_arg_type = self._attempt_type_instance_aqqusition(arg_token)
            if actual_arg_type:
                self.arg_type_refs.append(actual_arg_type)
            else:
                self.arg_type_refs.append(None)
                self._add_type_error(arg_token)
