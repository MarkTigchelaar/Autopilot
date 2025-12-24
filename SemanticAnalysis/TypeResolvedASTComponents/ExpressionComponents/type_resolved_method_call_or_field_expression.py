from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode


class TypeResolvedMethodCallOrFieldExpression(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)
        self.struct_name = raw_node.get_lhs_exp().accept_resolved_statement(parent)
        self.rhs_ref_list = []
        for field_or_method in raw_node.get_field_or_methods():
            self.rhs_ref_list.append(field_or_method.accept_resolved_statement(parent))


    def resolve_types(self):
        # Resolve the 'receiver' type first, then find the field/method on that type
        pass