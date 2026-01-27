from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import TypeResolvedStatementWithExpression


class TypeResolvedDeferStatement(TypeResolvedStatementWithExpression):
    def __init__(self, raw_node, error_manager, type_resolved_module, parent):
        super().__init__(raw_node.get_method_or_reassignment(), error_manager, type_resolved_module, parent)
        self.raw_defer_statement = raw_node

    # def resolve_types(self):
    #     self.resolved_deffered_statement.resolve_types()