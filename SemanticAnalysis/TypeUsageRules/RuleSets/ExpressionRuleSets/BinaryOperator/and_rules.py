from Tokenization.symbols import *
from SemanticAnalysis.TypeUsageRules.utils import make_key


VALID_AND_OPERATIONS_BOOL = {
    make_key(BOOL, UNDERSCORE, AND, UNDERSCORE, BOOL): BOOL
}

def make_and_rule_table() -> dict:
    and_rule_table = dict()
    and_rule_table.update(VALID_AND_OPERATIONS_BOOL)
    return and_rule_table
