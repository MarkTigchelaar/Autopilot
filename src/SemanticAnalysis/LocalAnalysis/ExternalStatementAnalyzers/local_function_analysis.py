from ErrorHandling.semantic_error_messages import *

def analyze_function(analyzer, ast_node, struct_fields = None):
    analyze_arg_names(analyzer, ast_node)
    analyze_return_paths(analyzer, ast_node)
    analyze_loop_branching_and_labels(analyzer, ast_node)

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
                analyzer.add_error(stmt.get_descriptor_token(), RETURN_NOT_LAST_STATEMENT)
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
    if has_path_with_no_return(analyzer, switch_statement.default_case.get_statements()):
        return True
    return False

def last_statement_in_block_is_default(stmt):
    return stmt.default_case is not None


# Need to check that breaks, and continues are actually inside loops.
# Also need to check that labels for break statements actually refer to a loop name.
def analyze_loop_branching_and_labels(analyzer, ast_node):
    loop_names = set()
    check_loop_logic(analyzer, ast_node.statements, loop_names, False)

def check_loop_logic(analyzer, statements, loop_names, in_loop = False):
    for stmt in statements:
        if str(stmt.__class__.__name__) in ("ForStatement", "LoopStatement", "WhileStatement"):
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
