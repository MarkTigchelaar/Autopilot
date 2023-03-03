import symbols
from ErrorHandling.semantic_error_messages import *
from SemanticAnalysis.analysis_utilities import get_token_literal

def analyze_import(analyzer, import_node):
    check_import_list_items(analyzer, import_node)
    check_import_path(analyzer, import_node)


def check_import_list_items(analyzer, import_node):
    import_items = import_node.import_list
    for i in range(len(import_items)):
        for j in range(i + 1, len(import_items)):
            if get_token_literal(import_items[i].name_token) == get_token_literal(import_items[j].name_token):
                analyzer.add_error(import_items[j].name_token, DUPLICATE_IMPORT)
            if get_token_literal(import_items[i].name_token) == get_token_literal(import_items[j].new_name_token):
                if get_token_literal(import_items[j].new_name_token) != "":
                    analyzer.add_error(import_items[j].new_name_token, IMPORT_NAME_ALIAS_COLLISION)
            if get_token_literal(import_items[i].new_name_token) == get_token_literal(import_items[j].new_name_token):
                if get_token_literal(import_items[i].new_name_token) == "":
                    continue
                analyzer.add_error(import_items[j].new_name_token, DUPLICATE_IMPORT_ALIAS)
        if get_token_literal(import_items[i].name_token) == get_token_literal(import_items[i].new_name_token):
            analyzer.add_error(import_items[i].name_token, IMPORT_NAME_ALIAS_COLLISION)


# The rule is, you can only go upwards once (as in continue to go upwards), then down
# When you start by going down into sub folders, going up is an error
def check_import_path(analyzer, import_node):
    import_path = import_node.path_list
    dot_or_colon_found = False
    for node in import_path:
        if node.direction_token and node.direction_token.type_symbol in (symbols.DOT, symbols.COLON):
            dot_or_colon_found = True
        if node.direction_token and node.direction_token.type_symbol == symbols.RANGE:
            if dot_or_colon_found:
                analyzer.add_error(node.direction_token, PATH_BACKTRACKING)
                break
