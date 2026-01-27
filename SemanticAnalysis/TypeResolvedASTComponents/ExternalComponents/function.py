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
            raw_node.get_header(), self.error_manager, self.type_resolved_module, self
        )
        self.struct_fields = []

    def resolve_types(self):
        self.resolved_header.resolve_types()
        super().resolve_types()

    def add_struct_fields(self, struct_fields):
        self.struct_fields = struct_fields

    def _find_local_variable_by_name(self, value_name_token):
        arguments = self.resolved_header.get_arguments()
        for arg in arguments:
            if arg.get_name().literal == value_name_token.literal:
                return arg.get_verifiable_type()
        for field in self.struct_fields:
            if field.get_name().literal == value_name_token.literal:
                return arg.get_verifiable_type()
        
        for assignment_statement in self.assignment_statements:
            if assignment_statement.get_name().literal == value_name_token.literal:
                return assignment_statement
        
        for branch_logic_declare in self.branching_logic_contained_assignment_statements:
            if branch_logic_declare.get_name().literal == value_name_token.literal:
                return branch_logic_declare
        return None
