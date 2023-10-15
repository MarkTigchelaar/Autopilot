import symbols
from ..parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.InternalStatementParsing.assignment_parsing import parse_assignment
from Parsing.InternalStatementParsing.re_assignment_or_call_parsing import (
    parse_re_assignment_or_call,
    parse_defer,
)

# Imports below brought into statements due to circular import issue


def parse_statements(driver, in_if_or_elif=False):
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        driver.add_error(peek_token, EMPTY_STATEMENT)
        return None
    statement_list = list()
    while is_statement_token(peek_token):
        if secondary_branching_logic(peek_token):
            if in_if_or_elif:
                break
            else:
                driver.add_error(peek_token, UNEXPECTED_TOKEN)
        stmt = statement_step(driver)
        peek_token = driver.peek_token()
        if stmt is not None:
            statement_list.append(stmt)
        if driver.has_errors():
            return None
        if peek_token.type_symbol == symbols.ENDSCOPE:
            # parent statement / function/ unit test handles the END token
            break
    if len(statement_list) == 0 and not driver.has_errors():
        driver.add_error(peek_token, EMPTY_STATEMENT)
    if driver.has_errors():
        return None
    return statement_list


def is_statement_token(peek_token):
    if is_eof_type(peek_token):
        return False
    if peek_token.type_symbol == symbols.CASE:
        return False
    if peek_token.type_symbol == symbols.DEFAULT:
        return False
    return True


def secondary_branching_logic(peek_token):
    if peek_token.type_symbol == symbols.ELIF:
        return True
    if peek_token.type_symbol == symbols.ELSE:
        return True
    return False


def statement_step(driver):
    peek_token = driver.peek_token()
    stmt = None
    if peek_token.type_symbol == symbols.LET:
        stmt = parse_assignment(driver)
    elif peek_token.type_symbol == symbols.VAR:
        stmt = parse_assignment(driver)
    elif peek_token.type_symbol == symbols.DEFER:
        stmt = parse_defer(driver)
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        stmt = parse_re_assignment_or_call(driver)
    elif peek_token.type_symbol == symbols.IF:
        from Parsing.InternalStatementParsing.if_parsing import parse_if

        stmt = parse_if(driver)
    elif peek_token.type_symbol == symbols.ELIF:
        return None
    elif peek_token.type_symbol == symbols.ELSE:
        return None
    elif peek_token.type_symbol == symbols.UNLESS:
        from Parsing.InternalStatementParsing.unless_parsing import parse_unless

        stmt = parse_unless(driver)
    elif peek_token.type_symbol == symbols.LOOP:
        from Parsing.InternalStatementParsing.loop_parsing import parse_loop

        stmt = parse_loop(driver)
    elif peek_token.type_symbol == symbols.WHILE:
        from Parsing.InternalStatementParsing.while_parsing import parse_while

        stmt = parse_while(driver)
    elif peek_token.type_symbol == symbols.FOR:
        from Parsing.InternalStatementParsing.for_parsing import parse_for

        stmt = parse_for(driver)
    elif peek_token.type_symbol == symbols.RETURN:
        from Parsing.InternalStatementParsing.return_parsing import parse_return

        stmt = parse_return(driver)
    elif peek_token.type_symbol == symbols.BREAK:
        from Parsing.InternalStatementParsing.break_parsing import parse_break

        stmt = parse_break(driver)
    elif peek_token.type_symbol == symbols.CONTINUE:
        from Parsing.InternalStatementParsing.continue_parsing import parse_continue

        stmt = parse_continue(driver)
    elif peek_token.type_symbol == symbols.SWITCH:
        from Parsing.InternalStatementParsing.switch_parsing import parse_switch

        stmt = parse_switch(driver)
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return None
    elif is_external_keyword(peek_token):
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None
    elif is_primitive_type(peek_token):
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None
    elif is_primitive_literal(peek_token):
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None
    else:
        # out of context keywords, struct, int, ==, etc
        return None

    if stmt is None and not driver.has_errors():
        raise Exception("INTERNAL ERROR: no errors raised, but statement is None.")
    return stmt
