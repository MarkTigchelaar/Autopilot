from ErrorHandling.semantic_error_messages import *

def analyze_break(analyzer, ast_node):
    if not analyzer.currently_in_loop():
        analyzer.add_error(ast_node.get_descriptor_token(), INVALID_BREAK)

    if ast_node.label_name_token is None:
        return
    elif analyzer.is_loop_name_defined(ast_node.label_name_token):
        return
    analyzer.add_error(ast_node.label_name_token, UNDEFINED_LOOP_NAME)
