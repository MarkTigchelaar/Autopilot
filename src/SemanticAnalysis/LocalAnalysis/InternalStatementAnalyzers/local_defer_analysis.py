from local_reassign_analysis import analyze_reassign


def analyze_defer(analyzer, ast_node):
    analyze_reassign(analyzer, ast_node)
