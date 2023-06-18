import symbols
from ..parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.expression_parsing import parse_expression
from Parsing.InternalStatementParsing.statement_parsing import parse_statements
from Parsing.ASTComponents import ast_node_keys


def parse_if(driver):
    if_token = driver.next_token()
    enforce_if(if_token)
    peek_token = driver.peek_token()
    if_statement = driver.make_node(ast_node_keys.IF_STMT)
    if_statement.add_descriptor_token(if_token)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.LET:
        return assign_type_step(driver, if_statement)
    elif peek_token.type_symbol == symbols.VAR:
        return assign_type_step(driver, if_statement)
    else:
        return expression_step(driver, if_statement)


def expression_step(driver, if_statement):
    exp_ast = parse_expression(driver)
    if exp_ast is None:
        return None
    elif driver.has_errors():
        return None
    if_statement.add_expression(exp_ast)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.DO:
        return do_step(driver, if_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def assign_type_step(driver, if_statement):
    assign_type_token = driver.next_token()
    if_statement.add_assignment_type(assign_type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return unwrapped_option_variable_step(driver, if_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def unwrapped_option_variable_step(driver, if_statement):
    variable_token = driver.next_token()
    if_statement.add_variable_name(variable_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.EQUAL:
        return equal_step(driver, if_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def equal_step(driver, if_statement):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return option_name_step(driver, if_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def option_name_step(driver, if_statement):
    option_name_token = driver.next_token()
    if_statement.add_optional_name(option_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.DO:
        return do_step(driver, if_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def do_step(driver, if_statement):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    else:
        return statements_step(driver, if_statement)


def statements_step(driver, if_statement):
    stmts = parse_statements(driver, True)
    if driver.has_errors():
        return None
    if_statement.add_statements(stmts)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.ELIF:
        from Parsing.InternalStatementParsing.elif_parsing import parse_elif
        #return if_statement
        next_stmt_in_block = parse_elif(driver)
        if_statement.add_next_statement_in_block(next_stmt_in_block)
        return if_statement
    elif peek_token.type_symbol == symbols.ELSE:
        from Parsing.InternalStatementParsing.else_parsing import parse_else
        next_stmt_in_block = parse_else(driver)
        if_statement.add_next_statement_in_block(next_stmt_in_block)
        return if_statement
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return end_step(driver, if_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, if_statement):
    driver.discard_token()
    return if_statement


def enforce_if(if_token):
    if if_token.type_symbol != symbols.IF:
        raise Exception("INTERNAL ERROR: expected if statement, got " + if_token.literal)
