from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode



class TypeResolvedCollectionAccessExpression(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)
        self.collection_name = raw_node.get_name().accept_resolved_statement(parent)
        self.access_arguments = []
        for arg in raw_node.get_argument_list():
            self.access_arguments.append(arg.accept_resolved_statement(parent))

    def resolve_types(self):
        # e.g., list[0]
        pass