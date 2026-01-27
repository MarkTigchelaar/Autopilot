from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import (
    TypeResolvedASTNode,
)

from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_if_statement import (
    TypeResolvedIfStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_elif_statement import (
    TypeResolvedElifStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_else_statement import (
    TypeResolvedElseStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_unless_statement import (
    TypeResolvedUnlessStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_loop_statement import (
    TypeResolvedLoopStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_while_statement import (
    TypeResolvedWhileStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_for_statement import (
    TypeResolvedForStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_break_statement import (
    TypeResolvedBreakStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_continue_statement import (
    TypeResolvedContinueStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_return_statement import (
    TypeResolvedReturnStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_assignment_statement import (
    TypeResolvedAssignmentStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_reassignment_statement import (
    TypeResolvedReAssignmentStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_method_call_statement import (
    TypeResolvedMethodCallStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_defer_statement import (
    TypeResolvedDeferStatement,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.type_resolved_switch_statement import (
    TypeResolvedSwitchStatement,
    TypeResolvedCaseStatement,
)


class FunctionBody(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, type_resolved_module, parent):
        super().__init__(raw_node, error_manager, type_resolved_module, parent)
        self.resolved_statements = []
        self.assignment_statements = []
        self.branching_logic_contained_assignment_statements = []
        for statement in self.raw_node.get_statements():
            resolved_statement = statement.accept_resolved_function(self)
            self.resolved_statements.append(resolved_statement)


    def resolve_types(self):
        for resolved_statement in self.resolved_statements:
            resolved_statement.resolve_types()
            self.branching_logic_contained_assignment_statements.extend(
                resolved_statement.get_variable_declarations()
            )

    def make_if_statement(self, raw_node) -> TypeResolvedIfStatement:
        return TypeResolvedIfStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )

    def make_elif_statement(self, raw_node) -> TypeResolvedElifStatement:
        return TypeResolvedElifStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )


    def make_else_statement(self, raw_node) -> TypeResolvedElseStatement:
        return TypeResolvedElseStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )

    def make_unless_statement(self, raw_node) -> TypeResolvedUnlessStatement:
        return TypeResolvedUnlessStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )

    def make_loop_statement(self, raw_node) -> TypeResolvedLoopStatement:
        return TypeResolvedLoopStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )

    def make_while_statement(self, raw_node) -> TypeResolvedWhileStatement:
        return TypeResolvedWhileStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )

    def make_for_statement(self, raw_node) -> TypeResolvedForStatement:
        for_loop = TypeResolvedForStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )
        variable_declaration_list = for_loop.get_variable_declarations()
        self.branching_logic_contained_assignment_statements.extend(
            variable_declaration_list
        )
        return for_loop

    def make_break_statement(self, raw_node) -> TypeResolvedBreakStatement:
        return TypeResolvedBreakStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )

    def make_continue_statement(self, raw_node) -> TypeResolvedContinueStatement:
        return TypeResolvedContinueStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )

    def make_return_statement(self, raw_node) -> TypeResolvedReturnStatement:
        return TypeResolvedReturnStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )

    def make_assignment_statement(self, raw_node) -> TypeResolvedAssignmentStatement:
        assignment_statement = TypeResolvedAssignmentStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )
        self.assignment_statements.append(assignment_statement)
        return assignment_statement

    def make_reassignment_statement(
        self, raw_node
    ) -> TypeResolvedReAssignmentStatement:
        reassignment_statement = TypeResolvedReAssignmentStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )
        for assignment_statement in self.assignment_statements:
            reassignment_statement.match_assignment_statement(assignment_statement)
        return reassignment_statement

    def make_method_call_statement(self, raw_node) -> TypeResolvedMethodCallStatement:
        return TypeResolvedMethodCallStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )

    def make_defer_statement(self, raw_node) -> TypeResolvedDeferStatement:
        return TypeResolvedDeferStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )

    def make_switch_statement(self, raw_node) -> TypeResolvedSwitchStatement:
        return TypeResolvedSwitchStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )

    def make_case_statement(self, raw_node) -> TypeResolvedCaseStatement:
        return TypeResolvedCaseStatement(
            raw_node, self.error_manager, self.type_resolved_module, self
        )
