from Tokenization.symbols import *
from SemanticAnalysis.TypeUsageRules.utils import make_key


VALID_NAND_OPERATIONS_BOOL = {
    make_key(BOOL, UNDERSCORE, NAND, UNDERSCORE, BOOL): BOOL
}

def make_nand_rule_table() -> dict:
    nand_rule_table = dict()
    nand_rule_table.update(VALID_NAND_OPERATIONS_BOOL)
    return nand_rule_table