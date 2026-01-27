from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import TypeResolvedStatementWithExpression


class TypeResolvedReAssignmentStatement(TypeResolvedStatementWithExpression):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)
        self.assignment_statement = None
    
    def resolve_types(self):
        # Check if new value type matches the variable's original type
        # in next pass
        super().resolve_types()

    def match_assignment_statement(self, assignment_statement):
        variable_name = assignment_statement.get_variable_name()
        if variable_name.literal == self.raw_node.get_name().literal:
            if self.assignment_statement:
                raise Exception("Assignment statement already found")
            self.assignment_statement = assignment_statement
