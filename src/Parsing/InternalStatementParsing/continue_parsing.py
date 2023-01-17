import symbols
from ..parsing_utilities import *
from ErrorHandling.parsing_error_messages import *
from Parsing.ASTComponents import ast_node_keys

def parse_continue(driver):
    continue_token = driver.next_token()
    enforce_continue(continue_token)
    c_stmt = driver.make_node(ast_node_keys.CONT_STMT)
    c_stmt.add_descriptor_token(continue_token)
    return c_stmt


def enforce_continue(continue_token):
    if continue_token.type_symbol != symbols.CONTINUE:
        raise Exception("INTERNAL ERROR: expected continue statement, got " + continue_token.literal)
