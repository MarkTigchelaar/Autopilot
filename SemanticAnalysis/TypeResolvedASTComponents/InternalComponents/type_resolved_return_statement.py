from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import TypeResolvedStatementWithExpression


class TypeResolvedReturnStatement(TypeResolvedStatementWithExpression):

    def resolve_types(self):
        # Check if returned type matches function signature return type
        super().resolve_types()