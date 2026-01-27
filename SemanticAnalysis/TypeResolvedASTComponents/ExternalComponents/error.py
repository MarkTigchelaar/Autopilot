from Tokenization.symbols import STRING
from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode



class TypeResolvedError(TypeResolvedASTNode):

    def resolve_types(self):
        self.type_resolved_module.get_primitive_by_symbol_type(STRING)
        self._set_verified_raw_type_reference(self.string_ref)