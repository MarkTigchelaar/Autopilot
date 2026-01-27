from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import TypeResolvedStatementWithExpression



class TypeResolvedAssignmentStatement(TypeResolvedStatementWithExpression):
    def resolve_types(self):
        super().resolve_types()
        type_token = self.raw_node.get_type()
        if type_token:
            resolved_type = self._attempt_type_instance_aqqusition(type_token)
            if resolved_type:
                self._set_verified_raw_type_reference(resolved_type)
            else:
                self._add_type_error(type_token)

    def get_name(self):
        return self.raw_node.get_name()
    

    def check_type_usage(self):
        pass



