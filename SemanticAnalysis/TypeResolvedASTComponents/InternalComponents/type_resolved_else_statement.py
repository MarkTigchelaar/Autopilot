from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import TypeResolvedBranchingLogicWithExpressions

class TypeResolvedElseStatement(TypeResolvedBranchingLogicWithExpressions):
    def resolve_types(self):
        super().resolve_types()