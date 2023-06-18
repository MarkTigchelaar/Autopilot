from LocalAnalysis.ExpressionAnalyzers.entry_point import analyze_expression
# let a as int = 1
# var b = t
# var a: long = a <- error
# let b: int = a <- error
def analyze_assignment(analyzer, ast_node):
    analyze_expression(analyzer, ast_node.exp_ast)
