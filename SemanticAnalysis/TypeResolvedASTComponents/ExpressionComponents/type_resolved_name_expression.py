from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode


class TypeResolvedNameExpression(TypeResolvedASTNode):
    def resolve_types(self):
        # Resolve if this is a literal (constant) or a variable name
        # If variable, link back to the Assignment or Argument definition
        pass