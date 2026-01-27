from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import TypeResolvedBranchingLogic


class TypeResolvedLoopStatement(TypeResolvedBranchingLogic):
    def resolve_types(self):
        super().resolve_types()