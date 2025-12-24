import Tokenization.symbols as symbols
from Parsing.InternalStatementParsing.statement_parsing import parse_statements
from Parsing.utils import is_eof_type
from ErrorHandling.parsing_error_messages import *
from ASTComponents.ExternalComponents.unittest_statement import UnittestStatement



def parse_unittest(driver):
    unittest_token = driver.next_token()
    enforce_unittest(unittest_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.IDENTIFIER:
        return test_name_step(driver)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def test_name_step(driver):
    name_token = driver.next_token()
    unittest_stmt = UnittestStatement()
    unittest_stmt.add_test_name(name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.DO:
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
    if driver.is_unit_testing():
        statements = []
    else:
        statements = parse_statements(driver)
    if driver.has_errors():
        return None
    unittest_stmt.add_statements(statements)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.internal_type == symbols.ENDSCOPE:
        return end_step(driver, unittest_stmt)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, unittest_stmt):
    driver.discard_token()
    return unittest_stmt


def enforce_unittest(unittest_token):
    if unittest_token.internal_type != symbols.UNITTEST:
        raise Exception("INTERNAL ERROR: exprected unittest statemnt, got " + unittest_token.literal)
