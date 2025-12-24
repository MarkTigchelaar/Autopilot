import Tokenization.symbols as symbols
from ASTComponents.InternalComponents.continue_statement import ContinueStatement

def parse_continue(driver):
    continue_token = driver.next_token()
    enforce_continue(continue_token)
    c_stmt = ContinueStatement()
    c_stmt.add_descriptor_token(continue_token)
    return c_stmt


def enforce_continue(continue_token):
    if continue_token.internal_type != symbols.CONTINUE:
        raise Exception("INTERNAL ERROR: expected continue statement, got " + continue_token.literal)
