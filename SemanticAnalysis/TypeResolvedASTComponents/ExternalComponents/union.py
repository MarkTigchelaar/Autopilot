from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode


class TypeResolvedUnion(TypeResolvedASTNode):

    def __init__(self, raw_node, error_manager, type_annontated_module, parent):
        super().__init__(raw_node, error_manager, type_annontated_module, parent)
        self.member_types = []

    def resolve_types(self):
        for field in self.raw_node.get_fields():
            actual_type = self._attempt_type_instance_aqqusition(field.get_type())
            if actual_type:
                self.member_types.append(actual_type)
            else:
                self._add_type_error(field.get_type())
