from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import (
    TypeResolvedBranchingLogicWithExpressions,
    TypeResolvedBranchingDeclaration,
)


class TypeResolvedIfStatement(TypeResolvedBranchingLogicWithExpressions):

    def resolve_types(self):
        super().resolve_types()
        self.wrapped_option_variable_ast_node = None
        self.primitive_reference = None
        self.resolved_optional_type_declaration = None
        if self.raw_node.is_option_type():
            optional_token = self.raw_node.get_optional_name()
            self.wrapped_option_variable_ast_node = self._find_local_variable_by_name(
                optional_token
            )
            if not self.wrapped_option_variable_ast_node:
                self.primitive_reference = self._attempt_primitive_type_aqquisition(
                    optional_token
                )
                if self.primitive_reference:
                    return
                raise Exception("Variable_declaration not found")
                #self._add_type_error(optional_token)
            else:
                unwrapped_variable_name = (
                    self.raw_node.get_variable_name()
                )
                declaraton = TypeResolvedBranchingDeclaration(
                    unwrapped_variable_name, self.wrapped_option_variable_ast_node
                )
                self.resolved_optional_type_declaration = declaraton

    def get_variable_declarations(self):
        if not self.raw_node.is_option_type():
            return []
        return [self.resolved_optional_type_declaration]
