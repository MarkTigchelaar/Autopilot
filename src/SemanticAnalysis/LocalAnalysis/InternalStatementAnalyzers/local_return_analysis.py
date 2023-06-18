from ExpressionAnalyzers.entry_point import analyze_expression


def analyze_return(analyzer, ast_node):
    analyze_expression(analyzer, ast_node)
