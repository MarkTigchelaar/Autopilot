from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.function_body import (
    FunctionBody,
)


class TypeResolvedUnitTest(FunctionBody):
    def __init__(self, raw_node, error_manager, type_resolved_module, parent):
        super().__init__(raw_node, error_manager, type_resolved_module, parent)
        self.test_name = raw_node.get_name_token()
