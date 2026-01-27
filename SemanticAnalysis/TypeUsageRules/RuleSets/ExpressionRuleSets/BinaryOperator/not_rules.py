from Tokenization.symbols import *
from SemanticAnalysis.TypeUsageRules.utils import make_key


VALID_NOT_OPERATIONS_BOOL = {
    make_key(BOOL, UNDERSCORE, NOT, UNDERSCORE, BOOL): BOOL
}

def make_not_rule_table() -> dict:
    not_rule_table = dict()
    not_rule_table.update(VALID_NOT_OPERATIONS_BOOL)
    return not_rule_table