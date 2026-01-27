from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.addition_rules import make_addition_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.subtraction_rules import make_subtraction_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.multiplication_rules import make_multiplication_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.division_rules import make_division_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.exponent_rules import make_exponent_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.modulus_rules import make_modulus_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.not_equal_rules import make_not_equal_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.equal_rules import make_equal_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.greater_rules import make_greater_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.greater_equal_rules import make_greater_equal_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.lesser_equal_rules import make_lesser_equal_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.lesser_rules import make_lesser_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.and_rules import make_and_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.nand_rules import make_nand_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.or_rules import make_or_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.xor_rules import make_xor_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.nor_rules import make_nor_rule_table
from SemanticAnalysis.TypeUsageRules.RuleSets.ExpressionRuleSets.BinaryOperator.not_rules import make_not_rule_table

import Tokenization.symbols as symbols

class BinaryOperatorRuleSet:
    def __init__(self):
        self.add_rules = make_addition_rule_table()
        self.subtract_rules = make_subtraction_rule_table()
        self.multiply_rules = make_multiplication_rule_table()
        self.division_rules = make_division_rule_table()
        self.exponent_rules = make_exponent_rule_table()
        self.modulus_rules = make_modulus_rule_table()
        self.not_eq_rules = make_not_equal_rule_table()
        self.eq_rules = make_equal_rule_table()
        self.greater_rules = make_greater_rule_table()
        self.greater_equal_rules = make_greater_equal_rule_table()
        self.lesser_rules = make_lesser_rule_table()
        self.lesser_equal_rules = make_lesser_equal_rule_table()
        self.and_rules = make_and_rule_table()
        self.nand_rules = make_nand_rule_table()
        self.or_rules = make_or_rule_table()
        self.xor_rules = make_xor_rule_table()
        self.nor_rules = make_nor_rule_table()
        self.not_rules = make_not_rule_table()



    def check_full_operation_type_usage(self, op_token, key):
        match op_token.internal_type:
            case symbols.PLUS:
                if key in self.add_rules:
                    return self.add_rules[key]
                return None
            case symbols.MINUS:
                if key in self.subtract_rules:
                    return self.subtract_rules[key]
                return None
            case symbols.STAR:
                if key in self.multiply_rules:
                    return self.multiply_rules[key]
                return None
            case symbols.SLASH:
                if key in self.division_rules:
                    return self.division_rules[key]
                return None
            case symbols.CARROT:
                if key in self.exponent_rules:
                    return self.exponent_rules[key]
                return None
            case symbols.MOD:
                if key in self.modulus_rules:
                    return self.modulus_rules[key]
                return None
            case symbols.BANG_EQUAL:
                if key in self.not_eq_rules:
                    return self.not_eq_rules[key]
                return None
            case symbols.EQUAL_EQUAL:
                if key in self.eq_rules:
                    return self.eq_rules[key]
                return None
            case symbols.GREATER:
                if key in self.greater_rules:
                    return self.greater_rules[key]
                return None
            case symbols.GREATER_EQUAL:
                if key in self.greater_equal_rules:
                    return self.greater_equal_rules[key]
                return None
            case symbols.LESS:
                if key in self.lesser_rules:
                    return self.lesser_rules[key]
                return None
            case symbols.LESS_EQUAL:
                if key in self.lesser_equal_rules:
                    return self.lesser_equal_rules[key]
                return None
            case symbols.AND:
                if key in self.and_rules:
                    return self.and_rules[key]
                return None
            case symbols.NAND:
                if key in self.nand_rules:
                    return self.nand_rules[key]
                return None
            case symbols.OR:
                if key in self.or_rules:
                    return self.or_rules[key]
                return None
            case symbols.XOR:
                if key in self.xor_rules:
                    return self.xor_rules[key]
                return None
            case symbols.NOR:
                if key in self.nor_rules:
                    return self.nor_rules[key]
                return None
            case symbols.NOT:
                if key in self.not_rules:
                    return self.not_rules[key]
                return None
            case _:
                raise Exception(f"Unknown op token: {op_token}")
