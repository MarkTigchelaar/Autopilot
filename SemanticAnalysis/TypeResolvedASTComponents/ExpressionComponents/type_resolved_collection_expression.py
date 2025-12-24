from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode



class TypeResolvedCollectionExpression(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)
        self.collection_name = raw_node.get_lhs_type().accept_resolved_statement(parent)
        self.resolved_elements = []
        for element in raw_node.get_collection_elements():
            resolved_element = element.accept_resolved_statement(parent)
            self.resolved_elements.append(resolved_element)

    def resolve_types(self):
        # e.g., [1, 2, 3] or {"key": "value"}
        pass