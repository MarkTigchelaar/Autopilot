
def analyze_loop(analyzer, ast_node):
    from local_statement_analysis import analyze_statements
    analyze_statements(analyzer, ast_node.statements)
