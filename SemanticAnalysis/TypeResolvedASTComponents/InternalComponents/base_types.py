from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import (
    TypeResolvedASTNode,
)


from SemanticAnalysis.TypeResolvedASTComponents.ExpressionComponents.type_resolved_name_expression import (
    TypeResolvedNameExpression,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExpressionComponents.type_resolved_prefix_expression import (
    TypeResolvedPrefixExpression,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExpressionComponents.type_resolved_operator_expression import (
    TypeResolvedOperatorExpression,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExpressionComponents.type_resolved_function_call_expression import (
    TypeResolvedFunctionCallExpression,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExpressionComponents.type_resolved_collection_expression import (
    TypeResolvedCollectionExpression,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExpressionComponents.type_resolved_collection_access_expression import (
    TypeResolvedCollectionAccessExpression,
)
from SemanticAnalysis.TypeResolvedASTComponents.ExpressionComponents.type_resolved_method_call_or_field_expression import (
    TypeResolvedMethodCallOrFieldExpression,
)


class TypeResolvedStatementWithExpression(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, type_annontated_module, parent):
        super().__init__(raw_node, error_manager, type_annontated_module, parent)
        self.expression = self.raw_node.get_expression_ast().accept_resolved_statement(self)

    def resolve_types(self):
        self.expression.resolve_types()

    # --- Factory Methods for Expressions ---

    def make_name_expression(self, raw_node) -> TypeResolvedNameExpression:
        return TypeResolvedNameExpression(
            raw_node, self.error_manager, self.type_annontated_module, self
        )

    def make_prefix_expression(self, raw_node) -> TypeResolvedPrefixExpression:
        return TypeResolvedPrefixExpression(
            raw_node, self.error_manager, self.type_annontated_module, self
        )

    def make_operator_expression(self, raw_node) -> TypeResolvedOperatorExpression:
        return TypeResolvedOperatorExpression(
            raw_node, self.error_manager, self.type_annontated_module, self
        )

    def make_function_call_expression(
        self, raw_node
    ) -> TypeResolvedFunctionCallExpression:
        return TypeResolvedFunctionCallExpression(
            raw_node, self.error_manager, self.type_annontated_module, self
        )

    def make_collection_expression(self, raw_node) -> TypeResolvedCollectionExpression:
        return TypeResolvedCollectionExpression(
            raw_node, self.error_manager, self.type_annontated_module, self
        )

    def make_collection_access_expression(
        self, raw_node
    ) -> TypeResolvedCollectionAccessExpression:
        return TypeResolvedCollectionAccessExpression(
            raw_node, self.error_manager, self.type_annontated_module, self
        )

    def make_method_call_or_field_expression(
        self, raw_node
    ) -> TypeResolvedMethodCallOrFieldExpression:
        return TypeResolvedMethodCallOrFieldExpression(
            raw_node, self.error_manager, self.type_annontated_module, self
        )


class TypeResolvedBranchingLogicWithExpressions(TypeResolvedStatementWithExpression):
    def __init__(self, raw_node, error_manager, type_annontated_module, parent):
        super().__init__(raw_node, error_manager, type_annontated_module, parent)
        self.resolved_statements = []
        self.resolved_next_statement_in_block = None
        for statement in raw_node.get_statements():
            resolved_statement = statement.accept_resolved_function(parent)
            self.resolved_statements.append(resolved_statement)
        if raw_node.has_next_statement_in_block():
            next_statement = raw_node.get_next_statement_in_block()
            self.resolved_next_statement_in_block = (
                next_statement.accept_resolved_function(parent)
            )

    def resolve_types(self):
        super().resolve_types()
        for resolved_statement in self.resolved_statements:
            resolved_statement.resolve_types()
        if self.resolved_next_statement_in_block:
            self.resolved_next_statement_in_block.resolve_types()


class TypeResolvedBranchingLogic(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, type_annontated_module, parent):
        super().__init__(self, raw_node, error_manager, type_annontated_module, parent)
        self.resolved_statements = []
        self.resolved_next_statement_in_block = None
        for statement in raw_node.get_statements():
            resolved_statement = statement.accept_resolved_function(parent)
            self.resolved_statements.append(resolved_statement)
        if raw_node.has_next_statement_in_block():
            next_statement = raw_node.get_next_statement_in_block()
            self.resolved_next_statement_in_block = (
                next_statement.accept_resolved_function(parent)
            )

    def resolve_types(self):
        for resolved_statement in self.resolved_statements:
            resolved_statement.resolve_types()
        if self.resolved_next_statement_in_block:
            self.resolved_next_statement_in_block.resolve_types()
