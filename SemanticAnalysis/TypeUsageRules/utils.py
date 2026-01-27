from Tokenization.symbols import UNDERSCORE

def make_key(lhs, op, rhs) -> str:
    return lhs + UNDERSCORE + op + UNDERSCORE + rhs