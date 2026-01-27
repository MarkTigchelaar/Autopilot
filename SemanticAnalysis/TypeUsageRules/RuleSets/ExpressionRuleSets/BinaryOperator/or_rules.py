from Tokenization.symbols import *
from SemanticAnalysis.TypeUsageRules.utils import make_key


VALID_OR_OPERATIONS_BOOL = {
    make_key(BOOL, UNDERSCORE, OR, UNDERSCORE, BOOL): BOOL
}

def make_or_rule_table() -> dict:
    or_rule_table = dict()
    or_rule_table.update(VALID_OR_OPERATIONS_BOOL)
    return or_rule_table