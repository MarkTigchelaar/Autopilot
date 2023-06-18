from LocalAnalysis.ExpressionAnalyzers.entry_point import analyze_expression


# method / fields, or an expression
# l value must be a identifier, or a identifier with a []
# This can be done using the tables in global analysis
def analyze_reassign(analyzer, ast_node):
    analyze_expression(analyzer, ast_node.l_value_exp)
    analyze_expression(analyzer, ast_node.r_value_exp)
