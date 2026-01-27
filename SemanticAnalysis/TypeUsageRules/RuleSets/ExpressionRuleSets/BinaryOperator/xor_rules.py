from Tokenization.symbols import *
from SemanticAnalysis.TypeUsageRules.utils import make_key


VALID_XOR_OPERATIONS_BOOL = {
    make_key(BOOL, UNDERSCORE, XOR, UNDERSCORE, BOOL): BOOL
}

def make_xor_rule_table() -> dict:
    xor_rule_table = dict()
    xor_rule_table.update(VALID_XOR_OPERATIONS_BOOL)
    return xor_rule_table