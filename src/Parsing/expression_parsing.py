import symbols
from .parsing_utilities import *
from keywords import is_eof_type
from ErrorHandling.parsing_error_messages import *
from ASTComponents import ast_node_keys


# Pratt Parsing technique
def parse_expression(driver):
    ast = _parse(driver, 0)
    if driver.has_errors():
        return None
    return ast


def _parse(driver, precedence):
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        return None
    elif driver.has_errors():
        return None
    left_exp = parse_prefix_expression(driver)
    if left_exp is None:
        return None
    return parse_infix_sub_tree(driver, left_exp, precedence)


# LHS of the (sub) expression
def parse_prefix_expression(driver):
    token = driver.next_token()
    if token.type_symbol == symbols.MINUS:
        return parse_prefix(token, driver)
    elif token.type_symbol == symbols.NOT:
        return parse_prefix(token, driver)
    elif token.type_symbol == symbols.LEFT_PAREN:
        return parse_parenthesis(driver)
    elif token.type_symbol == symbols.LEFT_BRACKET:
        return parse_brackets(driver)
    elif token.type_symbol == symbols.LEFT_BRACE:
        return parse_curly_braces(driver)
    else:
        return parse_name(token, driver)


def parse_prefix(token, driver):
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif not is_valid_expression_token(peek_token):
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None
    rhs_expression = _parse(driver, PREFIX)
    if rhs_expression is None:
        return None
    else:
        prefix = driver.make_node(ast_node_keys.PREFIX_EXP)
        prefix.add_name(token)
        prefix.add_rhs_exp(rhs_expression)
        return prefix


def parse_parenthesis(driver):
    peek_token = driver.peek_token()

    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol == symbols.RIGHT_PAREN:
        driver.add_error(peek_token, EMPTY_EXP)
        return None

    expression = parse_expression(driver)
    if expression is None:
        return None

    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol != symbols.RIGHT_PAREN:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None
    driver.discard_token()
    return expression


def parse_brackets(driver):
    return parse_collection(driver, symbols.LEFT_BRACKET, symbols.RIGHT_BRACKET)


def parse_curly_braces(driver):
    return parse_collection(driver, symbols.LEFT_BRACE, symbols.RIGHT_BRACE)


def parse_collection(driver, lhs_type, rhs_type):
    expression_array = list()
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    if peek_token.type_symbol != rhs_type:
        while driver.peek_token().type_symbol != rhs_type:
            if out_of_place_collection_token(peek_token):
                driver.add_error(peek_token, UNEXPECTED_TOKEN)
                return None

            expression = parse_expression(driver)
            peek_token = driver.peek_token()
            if expression is None:
                break
            expression_array.append(expression)
            if peek_token.type_symbol != symbols.COMMA:
                break
            driver.discard_token()
            peek_token = driver.peek_token()
            if driver.peek_token().type_symbol == rhs_type:
                driver.add_error(driver.peek_token(), MISSING_COLLECTION_EXPRESSION)
    else:
        driver.add_error(peek_token, EMPTY_EXP)
        return None

    if driver.has_errors():
        return None
    elif is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol != rhs_type:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None
    driver.discard_token()
    collection = driver.make_node(ast_node_keys.COLLECT_EXP)
    collection.add_lhs_type(lhs_type)
    collection.add_expression(expression_array)
    collection.add_rhs_type(rhs_type)
    return collection


def parse_name(token, driver):
    if passes_expression_name_token_check(driver, token):
        name = driver.make_node(ast_node_keys.NAME_EXP)
        name.add_name(token)
        return name
    return None


def parse_infix_sub_tree(driver, left_exp, precedence):
    if driver.has_errors():
        return None
    while precedence < find_infix_precedence(driver.peek_token()):
        token = driver.next_token()
        left_exp = parse_infix_expression(driver, token, left_exp)
        if driver.has_errors():
            return None
        if left_exp == None:
            raise Exception(
                "INTERNAL ERROR: Could not parse infix expression "
                + driver.current_file()
            )
    return left_exp


def parse_infix_expression(driver, token, left_exp):
    if is_sum_type(token):
        return parse_binary_operator(SUM, driver, token, left_exp)
    elif is_product(token):
        return parse_binary_operator(PRODUCT, driver, token, left_exp)
    elif is_exponent(token):
        return parse_binary_operator(EXPONENT, driver, token, left_exp, True)
    elif is_hash_literal(token):
        return parse_binary_operator(HASHLITERAL, driver, token, left_exp)
    elif is_comparison_operator(token):
        return parse_binary_operator(COMPARISON, driver, token, left_exp)
    elif is_logical_operator(token):
        if is_prefix_logical_operator(token):
            driver.add_error(token, INVALID_PREFIX_USAGE)
            return None
        return parse_binary_operator(LOGICAL, driver, token, left_exp)
    elif is_function_call(token):
        return parse_function_call(driver, left_exp)
    elif is_collection_access_by_index(token):
        return parse_collection_access(driver, left_exp)
    elif is_field_accessor_operator(token):
        return parse_method_call_or_field_access(driver, token, left_exp)
    else:
        raise Exception(
            "INTERNAL ERROR: token past check, but still not recognized: "
            + token.to_string()
        )


def parse_binary_operator(precedence, driver, token, lhs_exp, right_associative=False):
    if right_associative:
        precedence -= 1
    rhs_exp = _parse(driver, precedence)
    if driver.has_errors():
        return None
    if rhs_exp is None:
        peek_token = driver.peek_token()
        if is_eof_type(peek_token):
            driver.add_error(peek_token, EOF_REACHED)
        return None
    operator = driver.make_node(ast_node_keys.OP_EXP)
    operator.add_name(token)
    operator.add_lhs_exp(lhs_exp)
    operator.add_rhs_exp(rhs_exp)
    return operator


def parse_function_call(driver, fn_name_exp):
    return fn_call_or_collection_access(driver, fn_name_exp, symbols.RIGHT_PAREN)


def parse_collection_access(driver, name_exp):
    return fn_call_or_collection_access(driver, name_exp, symbols.RIGHT_BRACKET)


def fn_call_or_collection_access(driver, name_exp, rhs_type):
    argument_list = list()
    while driver.peek_token().type_symbol != rhs_type:
        if out_of_place_collection_token(driver.peek_token()):
            driver.add_error(driver.peek_token(), UNEXPECTED_TOKEN)
            return None

        arg_exp = parse_expression(driver)
        if arg_exp is None:
            break
        argument_list.append(arg_exp)
        peek_token = driver.peek_token()

        if peek_token.type_symbol != symbols.COMMA:
            break
        driver.discard_token()
        if driver.peek_token().type_symbol == rhs_type:
            if rhs_type == symbols.RIGHT_PAREN:
                msg = MISSING_ARG_EXPRESSION
            else:
                msg = COLLECTION_ACCESS_MISSING_EXPRESSION
            driver.add_error(driver.peek_token(), msg)

    if driver.has_errors():
        return None
    peek_token = driver.peek_token()
    if is_eof_type(peek_token):
        driver.add_error(peek_token, EOF_REACHED)
        return None
    elif peek_token.type_symbol != rhs_type:
        driver.add_error(peek_token, UNEXPECTED_TOKEN)
        return None
    driver.discard_token()
    if rhs_type == symbols.RIGHT_PAREN:
        fn_call = driver.make_node(ast_node_keys.FN_CALL_EXP)
        fn_call.add_name_exp(name_exp)
        fn_call.add_argument_list(argument_list)
        return fn_call
    elif rhs_type == symbols.RIGHT_BRACKET:
        collection_access = driver.make_node(ast_node_keys.COLLECT_ACCESS_EXP)
        collection_access.add_name_exp(name_exp)
        collection_access.add_argument_list(argument_list)
        return collection_access
    else:
        raise Exception(
            "INTERNAL ERROR: closing symbol for collection access or function call not recognized: "
            + rhs_type
        )


def parse_method_call_or_field_access(driver, token, left_exp):
    field_or_method_list = list()
    while is_field_accessor_operator(token):
        if is_eof_type(driver.peek_token()):
            driver.add_error(driver.peek_token(), EOF_REACHED)
            return None
        field_or_method = _parse(driver, 0)
        field_or_method_list.append(field_or_method)
        token = driver.peek_token()
    if driver.has_errors():
        return None
    method_or_field = driver.make_node(ast_node_keys.METHOD_OR_FIELD_EXP)
    method_or_field.add_lhs_exp(left_exp)
    method_or_field.add_field_or_methods(field_or_method_list)
    return method_or_field
