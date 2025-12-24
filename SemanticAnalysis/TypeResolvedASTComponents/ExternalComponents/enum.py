from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode


class TypeResolvedEnum(TypeResolvedASTNode):

    def resolve_types(self):
        enum_type = self.raw_node.get_general_type()
        if enum_type is None:
            raise Exception("enum missing general type!")
        else:
            primitive_type_ref = self.type_annontated_module.get_primitive_by_item_type_name(enum_type)
        if primitive_type_ref is None:
            raise Exception("Could not identify primitive type for enum")
        self._set_verified_type_reference(primitive_type_ref)