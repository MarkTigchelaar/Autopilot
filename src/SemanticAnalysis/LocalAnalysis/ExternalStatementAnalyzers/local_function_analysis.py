from ErrorHandling.semantic_error_messages import *
from symbols import IDENTIFIER


def analyze_function(analyzer, ast_node, struct_fields=[]):
    # raise Exception("here")
    analyze_arg_names(analyzer, ast_node)
    analyze_return_paths(analyzer, ast_node)
    analyze_loop_branching_and_labels(analyzer, ast_node)
    analyze_variable_declarations(analyzer, ast_node, struct_fields)
    analyze_variable_usage(analyzer, ast_node, struct_fields)
    # analyze_loop_labels(analyzer, ast_node)


def analyze_arg_names(analyzer, ast_node):
    args = ast_node.header.arguments
    if args is None or len(args) < 1:
        return
    for i in range(len(args)):
        for j in range(i + 1, len(args)):
            if args[i].arg_name_token.literal == args[j].arg_name_token.literal:
                analyzer.add_error(args[j].arg_name_token, FUNCTION_ARG_NAME_COLLISION)


# If function returns something, then all code paths must end in a return statement
def analyze_return_paths(analyzer, ast_node):
    return_type_token = ast_node.header.return_type_token
    if return_type_token is None:
        return
    statements = ast_node.statements
    if has_path_with_no_return(analyzer, statements):
        analyzer.add_error(ast_node.header.name_token, FUNCTION_MISSING_RETURN_PATH)


# Whether the type being returned (if any) is correct,
# Is determined later using tables
# NOTE: This is a very expensive check to perform
def has_path_with_no_return(analyzer, statements):
    for i in range(len(statements)):
        is_last_stmt = i >= len(statements) - 1
        stmt = statements[i]
        if str(stmt.__class__.__name__) == "ReturnStatement":
            if not is_last_stmt:
                analyzer.add_error(
                    stmt.get_descriptor_token(), RETURN_NOT_LAST_STATEMENT
                )
            # means bad code, but it also means it's not missing a return path here!
            return False
        if str(stmt.__class__.__name__) == "IfStatement":
            dead_end = if_statement_chain_has_dead_end(analyzer, stmt)
            last_is_else = last_statement_in_block_is_else(stmt)
            if (not dead_end) and last_is_else and is_last_stmt:
                return False
            elif dead_end and is_last_stmt:
                return True
        elif str(stmt.__class__.__name__) == "SwitchStatement":
            dead_end = switch_statement_chain_has_dead_end(analyzer, stmt)
            last_is_default = last_statement_in_block_is_default(stmt)
            if (not dead_end) and last_is_default and is_last_stmt:
                return False
            elif dead_end and is_last_stmt:
                return True
        elif stmt.has_nested_statements():
            sub_statements = stmt.get_statements()
            if has_path_with_no_return(analyzer, sub_statements) and is_last_stmt:
                return True
    return True


def if_statement_chain_has_dead_end(analyzer, if_statement):
    stmt = if_statement
    while stmt is not None:
        if has_path_with_no_return(analyzer, stmt.get_statements()):
            return True
        stmt = stmt.next_statement_in_block
    return False


def last_statement_in_block_is_else(stmt):
    while stmt.next_statement_in_block is not None:
        stmt = stmt.next_statement_in_block
    if str(stmt.__class__.__name__) == "ElseStatement":
        return True
    return False


def switch_statement_chain_has_dead_end(analyzer, switch_statement):
    for case_statement in switch_statement.get_statements():
        if has_path_with_no_return(analyzer, case_statement.get_statements()):
            return True
    if not last_statement_in_block_is_default(switch_statement):
        return False
    if has_path_with_no_return(
        analyzer, switch_statement.default_case.get_statements()
    ):
        return True
    return False


def last_statement_in_block_is_default(stmt):
    return stmt.default_case is not None


# Need to check that breaks, and continues are actually inside loops.
# Also need to check that labels for break statements actually refer to a loop name.
def analyze_loop_branching_and_labels(analyzer, ast_node):
    loop_names = set()
    check_loop_logic(analyzer, ast_node.statements, loop_names, False)


def check_loop_logic(analyzer, statements, loop_names, in_loop=False):
    for stmt in statements:
        if str(stmt.__class__.__name__) in (
            "ForStatement",
            "LoopStatement",
            "WhileStatement",
        ):
            if stmt.loop_name:
                name = stmt.loop_name.literal
                if name in loop_names:
                    analyzer.add_error(stmt.loop_name, DUPLICATE_LOOP_NAME)
                else:
                    loop_names.add(name)
            check_loop_logic(analyzer, stmt.get_statements(), loop_names, True)
        elif str(stmt.__class__.__name__) == "ContinueStatement":
            if not in_loop:
                analyzer.add_error(stmt.get_descriptor_token(), CONTINUE_NOT_IN_LOOP)
        elif str(stmt.__class__.__name__) == "BreakStatement":
            if not in_loop:
                analyzer.add_error(stmt.get_descriptor_token(), BREAK_NOT_IN_LOOP)
            loop_name = stmt.label_name_token
            if loop_name and loop_name not in loop_names:
                analyzer.add_error(loop_name, LOOP_LABEL_UNDEFINED)
        elif str(stmt.__class__.__name__) == "IfStatement":
            check_loop_logic_in_statement_chain(analyzer, stmt, loop_names, in_loop)
        elif stmt.has_nested_statements():
            check_loop_logic(analyzer, stmt.get_statements(), loop_names, in_loop)


def check_loop_logic_in_statement_chain(analyzer, stmt, loop_names, in_loop):
    while stmt is not None:
        check_loop_logic(analyzer, stmt.get_statements(), loop_names, in_loop)
        stmt = stmt.next_statement_in_block


def analyze_variable_declarations(analyzer, ast_node, struct_fields):
    variables = list()
    for field in struct_fields:
        variables.append(field.field_name_token)

    statements = ast_node.statements
    check_declarations(analyzer, statements, variables)


def check_declarations(analyzer, statements, variables):
    pop_list = []
    for stmt in statements:
        if str(stmt.__class__.__name__) == "AssignmentStatement":
            check_if_variable_declared(analyzer, stmt.get_name(), variables)

            variables.append(stmt.get_name())
            pop_list.append(stmt.get_name())
        elif str(stmt.__class__.__name__) in ("IfStatement", "ElifStatement"):
            if not stmt.has_expression_ast():
                check_if_variable_declared(
                    analyzer, stmt.get_variable_name(), variables
                )
                variables.append(stmt.get_variable_name())
                check_declarations(analyzer, stmt.get_statements(), variables)
                variables.pop(variables.index(stmt.get_variable_name()))
                if stmt.has_next_statement_in_block():
                    check_declarations(
                        analyzer, [stmt.next_statement_in_block], variables
                    )
                # pop_list.append(stmt.get_variable_name())
            else:
                check_declarations(analyzer, stmt.get_statements(), variables)
                if stmt.has_next_statement_in_block():
                    check_declarations(
                        analyzer, [stmt.next_statement_in_block], variables
                    )
        elif str(stmt.__class__.__name__) == "ForStatement":
            if stmt.index_or_key_name_token:
                check_if_variable_declared(
                    analyzer, stmt.index_or_key_name_token, variables
                )
                variables.append(stmt.index_or_key_name_token)
                check_declarations(analyzer, stmt.get_statements(), variables)
                variables.pop(variables.index(stmt.index_or_key_name_token))
                # pop_list.append(stmt.index_or_key_name_token)
            if stmt.map_value_name_token:
                check_if_variable_declared(
                    analyzer, stmt.map_value_name_token, variables
                )
                variables.append(stmt.map_value_name_token)
                check_declarations(analyzer, stmt.get_statements(), variables)
                variables.pop(variables.index(stmt.map_value_name_token))
                # pop_list.append(stmt.map_value_name_token)
            if stmt.unwrapped_optional_variable_name:
                check_if_variable_declared(
                    analyzer, stmt.unwrapped_optional_variable_name, variables
                )
                variables.append(stmt.unwrapped_optional_variable_name)
                check_declarations(analyzer, stmt.get_statements(), variables)
                variables.pop(variables.index(stmt.unwrapped_optional_variable_name))
                # pop_list.append(stmt.unwrapped_optional_variable_name)
            if stmt.second_unwrapped_optional_variable_name:
                check_if_variable_declared(
                    analyzer, stmt.second_unwrapped_optional_variable_name, variables
                )
                variables.append(stmt.second_unwrapped_optional_variable_name)
                check_declarations(analyzer, stmt.get_statements(), variables)
                variables.pop(
                    variables.index(stmt.second_unwrapped_optional_variable_name)
                )
                # pop_list.append(stmt.second_unwrapped_optional_variable_name)
            # check_declarations(analyzer, stmt.get_statements(), variables)

        elif stmt.has_nested_statements():
            check_declarations(analyzer, stmt.get_statements(), variables)
    for var in pop_list:
        variables.pop(variables.index(var))


def check_if_variable_declared(analyzer, name, variables):
    for var in variables:
        if name.literal == var.literal:
            analyzer.add_error(name, DUPLICATE_DECLARATION, var)


def analyze_variable_usage(analyzer, ast_node, struct_fields):
    variables = list()
    for field in struct_fields:
        variables.append(field.field_name_token)

    for arg in ast_node.header.arguments:
        variables.append(arg.arg_name_token)

    statements = ast_node.statements
    check_usage(analyzer, statements, variables)


def check_usage(analyzer, statements, variables):
    pop_list = []
    for stmt in statements:
        if str(stmt.__class__.__name__) == "AssignmentStatement":
            variables.append(stmt.get_name())
            pop_list.append(stmt.get_name())
            check_expression_for_declared_variables(
                analyzer, stmt.get_expression_ast(), variables
            )
        elif str(stmt.__class__.__name__) == "ReturnStatement":
            if stmt.get_expression_ast() is not None:
                check_expression_for_declared_variables(
                    analyzer, stmt.get_expression_ast(), variables
                )
        elif str(stmt.__class__.__name__) == "IfStatement":
            check_expression_for_declared_variables_in_if_like_statement(
                analyzer, stmt, variables
            )
        elif str(stmt.__class__.__name__) == "ElifStatement":
            check_expression_for_declared_variables_in_if_like_statement(
                analyzer, stmt, variables
            )
        elif str(stmt.__class__.__name__) == "ElseStatement":
            check_usage(analyzer, stmt.get_statements(), variables)
        elif str(stmt.__class__.__name__) == "UnlessStatement":
            check_expression_for_declared_variables(
                analyzer, stmt.get_expression_ast(), variables
            )
            check_usage(analyzer, stmt.get_statements(), variables)
        elif str(stmt.__class__.__name__) == "LoopStatement":
            check_usage(analyzer, stmt.get_statements(), variables)
        elif str(stmt.__class__.__name__) == "WhileStatement":
            check_expression_for_declared_variables(
                analyzer, stmt.get_expression_ast(), variables
            )
            check_usage(analyzer, stmt.get_statements(), variables)
        elif str(stmt.__class__.__name__) == "ForStatement":
            check_expression_for_declared_variables_in_for_loop(
                analyzer, stmt, variables
            )
        elif str(stmt.__class__.__name__) == "SwitchStatement":
            check_expression_for_declared_variables(
                analyzer, stmt.get_test_expression(), variables
            )
            for case in stmt.get_statements():  # includes default case
                for value in case.get_values():
                    check_for_matching_variables(analyzer, value, variables)
                check_usage(analyzer, case.get_statements(), variables)

        elif str(stmt.__class__.__name__) == "ReassignmentOrMethodCall":
            check_expression_for_declared_variables(
                analyzer, stmt.l_value_exp, variables
            )
            if stmt.r_value_exp:
                check_expression_for_declared_variables(
                    analyzer, stmt.r_value_exp, variables
                )
        elif str(stmt.__class__.__name__) == "DeferStatement":
            check_expression_for_declared_variables(
                analyzer, stmt.method_call.l_value_exp, variables
            )
            if stmt.method_call.r_value_exp:
                check_expression_for_declared_variables(
                    analyzer, stmt.method_call.r_value_exp, variables
                )

    for var in pop_list:
        variables.pop(variables.index(var))


def check_expression_for_declared_variables_in_for_loop(analyzer, statement, variables):
    pop_list = []
    if statement.index_or_key_name_token:
        variables.append(statement.index_or_key_name_token)
        pop_list.append(statement.index_or_key_name_token)

    if statement.map_value_name_token:
        variables.append(statement.map_value_name_token)
        pop_list.append(statement.map_value_name_token)

    if statement.unwrapped_optional_variable_name:
        variables.append(statement.unwrapped_optional_variable_name)
        pop_list.append(statement.unwrapped_optional_variable_name)

    if statement.second_unwrapped_optional_variable_name:
        variables.append(statement.second_unwrapped_optional_variable_name)
        pop_list.append(statement.second_unwrapped_optional_variable_name)

    if statement.index_start_name:
        check_for_matching_variables(analyzer, statement.index_start_name, variables)

    if statement.index_stop_name:
        check_for_matching_variables(analyzer, statement.index_stop_name, variables)

    if statement.iter_size:
        check_for_matching_variables(analyzer, statement.iter_size, variables)

    if statement.collection_name:
        check_for_matching_variables(analyzer, statement.collection_name, variables)

    if statement.optional_collection_name:
        check_for_matching_variables(
            analyzer, statement.optional_collection_name, variables
        )

    check_usage(analyzer, statement.get_statements(), variables)
    for var in pop_list:
        variables.pop(variables.index(var))


def check_expression_for_declared_variables_in_if_like_statement(
    analyzer, statement, variables
):
    unwrapped_variable = None
    if statement.has_expression_ast():
        check_expression_for_declared_variables(
            analyzer, statement.get_expression_ast(), variables
        )
    else:
        unwrapped_variable = statement.get_variable_name()
        variables.append(unwrapped_variable)
        optional_variable = statement.get_optional_name()
        check_for_matching_variables(analyzer, optional_variable, variables)

    check_usage(analyzer, statement.get_statements(), variables)
    if unwrapped_variable:
        variables.pop(variables.index(unwrapped_variable))

    if statement.has_next_statement_in_block():
        check_usage(analyzer, [statement.next_statement_in_block], variables)


def check_expression_for_declared_variables(analyzer, expression, variables):
    if expression.has_left_expression():
        check_expression_for_declared_variables(
            analyzer, expression.get_lhs_exp(), variables
        )
    if expression.has_right_expression():
        check_expression_for_declared_variables(
            analyzer, expression.get_rhs_exp(), variables
        )

    if str(expression.__class__.__name__) == "CollectionAccessExpression":
        collection_name_exp = expression.get_name()
        collection_name_token = collection_name_exp.get_name()
        check_for_matching_variables(analyzer, collection_name_token, variables)
        elements = expression.get_argument_list()
        for element in elements:
            check_expression_for_declared_variables(analyzer, element, variables)
        if len(elements) != 1:
            analyzer.add_error(
                collection_name_token, COLLECTION_ACCESS_WITH_WRONG_NUMBER_OF_ARGUMENTS
            )

    elif str(expression.__class__.__name__) == "FunctionCallExpression":
        arguments = expression.get_argument_list()
        for arg in arguments:
            check_expression_for_declared_variables(analyzer, arg, variables)
    elif str(expression.__class__.__name__) == "MethodCallOrFieldExpression":
        # has lhs expression, first if catches that one
        # field_or_method_list = expression.get_field_or_methods()
        # for field_or_method in field_or_method_list:
        #     check_expression_for_declared_variables(analyzer, field_or_method, variables)
        return
        # fields and methods are not local variables
    elif str(expression.__class__.__name__) == "NameExpression":
        name_token = expression.get_name()
        check_for_matching_variables(analyzer, name_token, variables)
    elif str(expression.__class__.__name__) == "CollectionExpression":
        elements = expression.get_collection_elements()
        for element in elements:
            check_expression_for_declared_variables(analyzer, element, variables)
    elif str(expression.__class__.__name__) in (
        "OperatorExpression",
        "PrefixExpression",
    ):
        return
    else:
        raise Exception("Unknown expression type in function call expression")


def check_for_matching_variables(analyzer, name_token, variables):
    if name_token.get_type() != IDENTIFIER:
        return
    for var in variables:
        if name_token.literal == var.literal:
            # print(f"found match: {name_token.literal} and {var.literal}")
            return
    analyzer.add_error(name_token, UNDEFINED_VARIABLE)
