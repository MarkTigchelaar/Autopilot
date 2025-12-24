from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode



class TypeResolvedPrefixExpression(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)
        self.rhs_exp = raw_node.get_rhs_exp().accept_resolved_statement(parent)
        

    def resolve_types(self):
        # Example: !bool or -int
        pass