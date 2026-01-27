from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import (
    TypeResolvedStatementWithExpression,
)
class TypeResolvedMethodCallStatement(TypeResolvedStatementWithExpression):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)
        #self.function_call_or_method_chain = raw_node.get_l_value().accept_resolved_statement(parent)


    
    def resolve_types(self):
        super().resolve_types()
        #self.function_call_or_method_chain.resolve_types()
