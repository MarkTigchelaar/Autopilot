import symbols
from ..parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.InternalStatementParsing.statement_parsing import parse_statements
from Parsing.ASTComponents import ast_node_keys


def parse_unittest(driver):
    unittest_token = driver.next_token()
    enforce_unittest(unittest_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return test_name_step(driver)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def test_name_step(driver):
    name_token = driver.next_token()
    unittest_stmt = driver.make_node(ast_node_keys.UNITTEST_STMT)
    unittest_stmt.add_test_name(name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.DO:
        return do_step(driver, unittest_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def do_step(driver, unittest_stmt):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    statements = parse_statements(driver)
    if driver.has_errors():
        return None
    unittest_stmt.add_statements(statements)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return end_step(driver, unittest_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, unittest_stmt):
    driver.discard_token()
    return unittest_stmt


def enforce_unittest(unittest_token):
    if unittest_token.type_symbol != symbols.UNITTEST:
        raise Exception("INTERNAL ERROR: exprected unittest statemnt, got " + unittest_token.literal)
