from ErrorHandling.semantic_error_messages import *

# for a in b..c, d as test do
# for a in b as test do
# for a, b in dict do
# for let a in b do
# for let a, b in option do
def analyze_for_loop(analyzer, ast_node):
    if ast_node.index_or_key_name_token is None:
        raise Exception("INTERNAL ERROR: index/key/iteration variable is None")

    check_iteration_index_variable(analyzer, ast_node)
    check_start_index_variable(analyzer, ast_node)
    check_stop_index_variable(analyzer, ast_node)
    check_iteration_step_variable(analyzer, ast_node)
    check_collection_item_variable(analyzer, ast_node)
    check_collection_variable(analyzer, ast_node)
    check_optional_variable(analyzer, ast_node)
    check_second_optional_variable(analyzer, ast_node)


def check_iteration_index_variable(analyzer, ast_node):
    index_var = ast_node.index_or_key_name_token
    if ast_node.index_start_name is None:
        return
    if ast_node.index_start_name and not ast_node.index_stop_name:
        raise Exception("INTERNAL ERROR: for loop has start index, but no stop index")
    
    if index_var.literal == ast_node.index_start_name.literal:
        analyzer.add_error(ast_node.index_start_name, START_IDX_SHADOWS_INDEX_VAR)
    
    if index_var.literal == ast_node.index_stop_name.literal:
        analyzer.add_error(ast_node.index_stop_name, STOP_IDX_SHADOWS_INDEX_VAR)
    
    if ast_node.iter_size is not None:
        if index_var.literal == ast_node.iter_size.literal:
            analyzer.add_error(ast_node.iter_size, ITER_SIZE_SHADOWS_INDEX_VAR)
    
    if ast_node.loop_name is not None:
        if index_var.literal == ast_node.loop_name.literal:
            analyzer.add_error(ast_node.loop_name, LOOP_NAME_SHADOWS_INDEX_VAR)
    

def check_start_index_variable(analyzer, ast_node):
    start_index = ast_node.index_start_name
    if start_index is None:
        return

    if start_index.literal == ast_node.index_stop_name.literal:
        analyzer.add_error(ast_node.index_stop_name, STOP_IDX_SHADOWS_START_IDX)
    
    if ast_node.iter_size is not None:
        if start_index.literal == ast_node.iter_size.literal:
            analyzer.add_error(ast_node.iter_size, ITER_SIZE_SHADOWS_START_IDX)
    
    if ast_node.loop_name is not None:
        if start_index.literal == ast_node.loop_name.literal:
            analyzer.add_error(ast_node.loop_name, LOOP_NAME_SHADOWS_START_IDX)


def check_stop_index_variable(analyzer, ast_node):
    stop_index = ast_node.index_stop_name
    if stop_index is None:
        return

    if ast_node.iter_size is not None:
        if stop_index.literal == ast_node.iter_size.literal:
            analyzer.add_error(ast_node.iter_size, ITER_SIZE_SHADOWS_STOP_IDX)
    
    if ast_node.loop_name is not None:
        if stop_index.literal == ast_node.loop_name.literal:
            analyzer.add_error(ast_node.loop_name, LOOP_NAME_SHADOWS_STOP_IDX)


def check_iteration_step_variable(analyzer, ast_node):
    if ast_node.iter_size is None:
        return

    if ast_node.loop_name is not None:
        if ast_node.iter_size.literal == ast_node.loop_name.literal:
            analyzer.add_error(ast_node.loop_name, LOOP_NAME_SHADOWS_ITER_SIZE)


def check_collection_item_variable(analyzer, ast_node):
    if ast_node.collection_name is None:
        return
    collection_item = ast_node.index_or_key_name_token
    loop_name = ast_node.loop_name

    if ast_node.map_value_name_token is not None:
        if collection_item.literal == ast_node.map_value_name_token.literal:
            analyzer.add_error(ast_node.map_value_name_token, MAP_VALUE_NAME_SHADOWS_KEY_ITEM)

        if loop_name is not None:
            if collection_item.literal == loop_name.literal:
                analyzer.add_error(ast_node.loop_name, LOOP_NAME_SHADOWS_VALUE_ITEM)

    if collection_item.literal == ast_node.collection_name.literal:
        analyzer.add_error(ast_node.collection_name, COLLECTION_NAME_SHADOWS_ITEM)
    

def check_collection_variable(analyzer, ast_node):
    if ast_node.collection_name is None:
        return
    
    if ast_node.loop_name is not None:
        if ast_node.collection_name.literal == ast_node.loop_name.literal:
            analyzer.add_error(ast_node.loop_name, LOOP_NAME_SHADOWS_COLLECTION_NAME)


def check_optional_variable(analyzer, ast_node):
    if ast_node.unwrapped_optional_variable_name is None:
        return
    opt = ast_node.unwrapped_optional_variable_name
    loop_name = ast_node.loop_name

    if ast_node.second_unwrapped_optional_variable_name is not None:
        if opt.literal == ast_node.second_unwrapped_optional_variable_name.literal:
            analyzer.add_error(ast_node.second_unwrapped_optional_variable_name, SECOND_OPT_VAR_SHADOWS_OPT_VAR)
    
    if ast_node.optional_collection_name is None:
        raise Exception("INTERNAL ERROR: optional collection is not defined in context where it should be")

    if opt.literal == ast_node.optional_collection_name.literal:
        analyzer.add_error(ast_node.optional_collection_name, OPTIONAL_COLLECTION_NAME_SHADOWS_OPTIONAL_VARIABLE)

    if loop_name is not None:
        if opt.literal == ast_node.loop_name:
            analyzer.add_error(ast_node.loop_name, LOOP_NAME_SHADOWS_OPTIONAL_VARIABLE)


def check_second_optional_variable(analyzer, ast_node):
    if ast_node.second_unwrapped_optional_variable_name is None:
        return
    opt = ast_node.second_unwrapped_optional_variable_name
    loop_name = ast_node.loop_name

    if opt.literal == ast_node.optional_collection_name.literal:
        analyzer.add_error(ast_node.optional_collection_name, OPTIONAL_COLLECTION_NAME_SHADOWS_OPTIONAL_VALUE_VARIABLE)

    if loop_name is not None:
        if opt.literal == ast_node.loop_name:
            analyzer.add_error(ast_node.loop_name, LOOP_NAME_SHADOWS_OPTIONAL_VALUE_VARIABLE)

