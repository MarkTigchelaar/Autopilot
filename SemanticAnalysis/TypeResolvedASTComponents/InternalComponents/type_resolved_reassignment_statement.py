from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import TypeResolvedStatementWithExpression


class TypeResolvedReAssignmentStatement(TypeResolvedStatementWithExpression):
    # def __init__(self, raw_node, error_manager, module_collection, parent):
    #     self.raw_node = raw_node
    #     self.error_manager = error_manager
    #     self.module_collection = module_collection
    #     self.parent = parent
    
    def resolve_types(self):
        # Check if new value type matches the variable's original type
        pass