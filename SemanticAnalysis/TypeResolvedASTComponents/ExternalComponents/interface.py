from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import (
    TypeResolvedASTNode,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.function_header import (
    TypeResolvedHeader,
)


class TypeResolvedInterface(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, type_annontated_module, parent):
        super().__init__(raw_node, error_manager, type_annontated_module, parent)
        self.resolved_headers = []
        for header in self.raw_node.get_function_headers():
            resolved_header = TypeResolvedHeader(
                header, self.error_manager, self.type_annontated_module, self
            )
            self.resolved_headers.append(resolved_header)
        
    def resolve_types(self):
        for header in self.resolved_headers:
            header.resolve_types()
