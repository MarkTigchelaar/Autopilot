from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode


class TypeResolvedMethodCallOrFieldExpression(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)
        self.struct_or_function_name = raw_node.get_lhs_exp().accept_resolved_statement(parent)
        self.rhs_ref_list = []
        for field_or_method in raw_node.get_field_or_methods():
            self.rhs_ref_list.append(field_or_method.accept_resolved_statement(parent))


    def resolve_types(self):
        # Resolve the 'receiver' type first, then find the field/method on that type
        self.struct_or_function_name.resolve_types()
        # Cant resolve the fields / methods right now, save for type usage checks
        # A struct in another module which is being called might not have
        # been resolved yet.
        for field_or_method in self.rhs_ref_list:
            field_or_method.resolve_types_in_expressions()