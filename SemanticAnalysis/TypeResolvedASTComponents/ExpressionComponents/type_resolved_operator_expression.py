from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import (
    TypeResolvedASTNode,
)
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.binary_operator_ruleset import (
    BinaryOperatorRuleSet,
)
from SemanticAnalysis.TypeUsageRules.utils import make_key, make_half_key
import Tokenization.symbols as symbols
from ErrorHandling.semantic_error_messages import (
    TYPE_INCOMPATABLE_WITH_BIN_OP,
    TYPES_INCOMPATABLE_WITH_EACT_OTHER_IN_BIN_OP,
)


class TypeResolvedOperatorExpression(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)
        self.lhs_exp = raw_node.get_lhs_exp().accept_resolved_statement(parent)
        self.rhs_exp = raw_node.get_rhs_exp().accept_resolved_statement(parent)
        self.ruleset = BinaryOperatorRuleSet()

    def resolve_types(self):
        # Handles binary ops (1 + 1). Ask left and right for types.
        self.lhs_exp.resolve_types()
        self.rhs_exp.resolve_types()

    def resolve_types_in_expressions(self):
        self.lhs_exp.resolve_types_in_expressions()
        self.rhs_exp.resolve_types_in_expressions()

    def check_type_usage(self):
        operator_token = self.raw_node.get_name()
        operator_symbol = operator_token.internal_type
        lhs_type = self.lhs_exp.resolved_type.internal_type
        rhs_type = self.rhs_exp.resolved_type.internal_type
        key = make_key(lhs_type, operator_symbol, rhs_type)
        internal_type = self.ruleset.check_full_operation_type_usage(
            operator_token, key
        )
        if not internal_type:
            self.error_manager.add_error(
                operator_token,
                TYPES_INCOMPATABLE_WITH_EACT_OTHER_IN_BIN_OP,
                lhs_type_token=self.lhs_exp.resolved_type,
                rhs_type_token=self.rhs_exp.resolved_type,
            )
