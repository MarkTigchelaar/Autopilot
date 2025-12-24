from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import TypeResolvedBranchingLogicWithExpressions

class TypeResolvedIfStatement(TypeResolvedBranchingLogicWithExpressions):
    # def __init__(self, raw_node, error_manager, module_collection, parent):
    #     self.raw_node = raw_node
    #     self.error_manager = error_manager
    #     self.module_collection = module_collection
    #     self.parent = parent # Likely a TypeResolvedFunction or another Statement
    
    def resolve_types(self):
        # Validate that the condition evaluates to a Boolean
        pass