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
        pass