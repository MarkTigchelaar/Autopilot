from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import TypeResolvedBranchingLogicWithExpressions



class TypeResolvedWhileStatement(TypeResolvedBranchingLogicWithExpressions):
    def resolve_types(self):
        super().resolve_types()