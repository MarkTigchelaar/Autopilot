from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.function_body import (
    FunctionBody,
)

from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.function_header import (
    TypeResolvedHeader,
)


class TypeResolvedFunction(FunctionBody):
    def __init__(self, raw_node, error_manager, type_resolved_module, parent):
        super().__init__(raw_node, error_manager, type_resolved_module, parent)
        self.resolved_header = TypeResolvedHeader(
            raw_node.get_header(), self.error_manager, self.type_annontated_module, self
        )

    def resolve_types(self):
        self.resolved_header.resolve_types()
        super().resolve_types()
