from ErrorHandling.semantic_error_messages import *
from ExpressionAnalyzers.entry_point import analyze_expression
from local_elif_analysis import analyze_elif
from local_else_analysis import analyze_else

# if true do
# if let item = option do
def analyze_if(analyzer, ast_node):
    if ast_node.test_expression:
        check_regular_if(analyzer, ast_node)
    else:
        check_option_if(analyzer, ast_node)
    if ast_node.next_statement_in_block:
        analyze_branch(analyzer, ast_node.next_statement_in_block)


def check_regular_if(analyzer, ast_node):
    analyze_expression(analyzer, ast_node.test_expression)
    analyze_sub_statements(analyzer, ast_node)


def check_option_if(analyzer, ast_node):
    if ast_node.unwrapped_optional_variable_name.literal == ast_node.optional_variable_name.literal:
        analyzer.add_error(ast_node.unwrapped_optional_variable_name, UNWRAPPED_OPTION_SHADOWS_OPTION)
    analyze_sub_statements(analyzer, ast_node)


def analyze_sub_statements(analyzer, case):
    from local_statement_analysis import analyze_statement
    for stmt in case.statements:
        analyze_statement(analyzer, stmt)


def analyze_branch(analyzer, elif_or_else_stmt):
    if str(type(elif_or_else_stmt)) == "ElifStatement":
        analyze_elif(analyzer, elif_or_else_stmt)
    else:
        analyze_else(analyzer, elif_or_else_stmt)
