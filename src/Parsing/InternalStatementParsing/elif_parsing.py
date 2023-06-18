import symbols
from ..parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from Parsing.expression_parsing import parse_expression
from Parsing.InternalStatementParsing.statement_parsing import parse_statements
from Parsing.ASTComponents import ast_node_keys

# might fold this into if statement parsing
def parse_elif(driver):
    elif_token = driver.next_token()
    enforce_elif(elif_token)
    peek_token = driver.peek_token()
    elif_statement = driver.make_node(ast_node_keys.ELIF_STMT)
    elif_statement.add_descriptor_token(elif_token)
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.LET:
        return assign_type_step(driver, elif_statement)
    elif peek_token.type_symbol == symbols.VAR:
        return assign_type_step(driver, elif_statement)
    else:
        return expression_step(driver, elif_statement)


def expression_step(driver, elif_statement):
    exp_ast = parse_expression(driver)
    if exp_ast is None:
        return None
    elif driver.has_errors():
        return None
    elif_statement.add_expression(exp_ast)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.DO:
        return do_step(driver, elif_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def assign_type_step(driver, elif_statement):
    assign_type_token = driver.next_token()
    elif_statement.add_assignment_type(assign_type_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return unwrapped_option_variable_step(driver, elif_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def unwrapped_option_variable_step(driver, elif_statement):
    variable_token = driver.next_token()
    elif_statement.add_variable_name(variable_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.EQUAL:
        return equal_step(driver, elif_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def equal_step(driver, elif_statement):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.IDENTIFIER:
        return option_name_step(driver, elif_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def option_name_step(driver, elif_statement):
    option_name_token = driver.next_token()
    elif_statement.add_optional_name(option_name_token)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.DO:
        return do_step(driver, elif_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def do_step(driver, elif_statement):
    driver.discard_token()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    else:
        return statements_step(driver, elif_statement)


def statements_step(driver, elif_statement):
    stmts = parse_statements(driver, True)
    if driver.has_errors():
        return None
    elif_statement.add_statements(stmts)
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.ELIF:
        #return elif_statement
        next_stmt_in_block = parse_elif(driver)
        elif_statement.add_next_statement_in_block(next_stmt_in_block)
        return elif_statement
    elif peek_token.type_symbol == symbols.ELSE:
        from Parsing.InternalStatementParsing.else_parsing import parse_else
        next_stmt_in_block = parse_else(driver)
        elif_statement.add_next_statement_in_block(next_stmt_in_block)
        return elif_statement
    elif peek_token.type_symbol == symbols.ENDSCOPE:
        return end_step(driver, elif_statement)
    else:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None


def end_step(driver, elif_statement):
    driver.discard_token()
    return elif_statement


def enforce_elif(elif_token):
    if elif_token.type_symbol != symbols.ELIF:
        raise Exception("INTERNAL ERROR: expected elif statement, got " + elif_token.literal)
