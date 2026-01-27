from Tokenization.symbols import *
from SemanticAnalysis.TypeUsageRules.utils import make_key


VALID_NOR_OPERATIONS_BOOL = {
    make_key(BOOL, UNDERSCORE, NOR, UNDERSCORE, BOOL): BOOL
}

def make_nor_rule_table() -> dict:
    nor_rule_table = dict()
    nor_rule_table.update(VALID_NOR_OPERATIONS_BOOL)
    return nor_rule_table