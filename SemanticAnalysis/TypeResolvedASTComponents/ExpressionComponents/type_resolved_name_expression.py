from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode


class TypeResolvedNameExpression(TypeResolvedASTNode):

    def __init__(self, raw_node, error_manager, type_resolved_module, parent):
        super().__init__(raw_node, error_manager, type_resolved_module, parent)
        self.variable_ast_node = None
        self.primitive_reference = None

    def resolve_types(self):
        # Resolve if this is a literal (constant) or a variable name
        # If variable, link back to the Assignment or Argument definition
        name_token = self.raw_node.get_name()
        variable_reference = self.parent.parent._find_local_variable_by_name(name_token)
        if variable_reference:
            self.variable_ast_node = variable_reference
        else:
            self.primitive_reference = self._attempt_primitive_type_aqquisition(name_token)
            if self.primitive_reference:
                return
            raise Exception("Variable_declaration not found")
            #self._add_type_error(name_token)

    def get_name(self):
        return self.raw_node.get_name()
    
    def check_type_usage(self):
        return