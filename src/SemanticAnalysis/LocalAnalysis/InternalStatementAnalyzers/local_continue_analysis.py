from ErrorHandling.semantic_error_messages import *

def analyze_continue(analyzer, ast_node):
    if not analyzer.currently_in_loop():
        analyzer.add_error(ast_node.get_descriptor_token(), INVALID_CONTINUE)
