from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode


class TypeResolvedFunctionCallExpression(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)
        self.function_name = raw_node.get_name().accept_resolved_statement(parent)
        self.arguments = []
        for argument in raw_node.get_argument_list():
            type_resolved_arg = argument.accept_resolved_statement(parent)
            self.arguments.append(type_resolved_arg)

    def resolve_types(self):
        # Check argument types against function signature
        function_name_token = self.function_name.get_name()
        resolved_type = self._attempt_type_instance_aqqusition(function_name_token)
        if resolved_type:
            self._set_verified_raw_type_reference(resolved_type)
        else:
            self._add_type_error(function_name_token)
        for arg in self.arguments:
            arg.resolve_types()

    def resolve_types_in_expressions(self):
        for arg in self.arguments:
            arg.resolve_types()
