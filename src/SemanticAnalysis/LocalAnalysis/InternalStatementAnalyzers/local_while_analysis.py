from ExpressionAnalyzers.entry_point import analyze_expression

def analyze_while_loop(analyzer, ast_node):
    analyze_expression(analyzer, ast_node.test_expression)
    analyze_sub_statements(analyzer, ast_node)


def analyze_sub_statements(analyzer, ast_node):
    from local_statement_analysis import analyze_statements
    analyze_statements(analyzer, ast_node.statements)
