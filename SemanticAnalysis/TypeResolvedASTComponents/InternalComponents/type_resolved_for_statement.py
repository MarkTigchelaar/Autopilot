from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import TypeResolvedBranchingLogic



class TypeResolvedForStatement(TypeResolvedBranchingLogic):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        self.raw_node = raw_node
        self.error_manager = error_manager
        self.module_collection = module_collection
        self.parent = parent
    
    def resolve_types(self):
        # This is critical for type inference of the loop variable
        pass