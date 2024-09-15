from symbols import LEFT_BRACE, LEFT_BRACKET, RIGHT_BRACE, RIGHT_BRACKET, COLON


def visit_expression(expression_ast, compiled_module, var_namer, spaces):
    if str(expression_ast.__class__.__name__) == "OperatorExpression":
        visit_binary_operator_expression(
            expression_ast, compiled_module, var_namer, spaces
        )
    if str(expression_ast.__class__.__name__) == "NameExpression":
        left_expression = expression_ast.get_name()
        var_namer.push(left_expression.literal)
    if str(expression_ast.__class__.__name__) == "PrefixExpression":
        visit_prefix_expression(expression_ast, compiled_module, var_namer, spaces)
    if str(expression_ast.__class__.__name__) == "FunctionCallExpression":
        visit_function_call_expression(
            expression_ast, compiled_module, var_namer, spaces
        )
    if str(expression_ast.__class__.__name__) == "CollectionExpression":
        visit_collection_expression(expression_ast, compiled_module, var_namer, spaces)
    if str(expression_ast.__class__.__name__) == "CollectionAccessExpression":
        visit_collection_access_expression(
            expression_ast, compiled_module, var_namer, spaces
        )
    if str(expression_ast.__class__.__name__) == "MethodCallOrFieldExpression":
        visit_method_call_or_field_expression(
            expression_ast, compiled_module, var_namer, spaces
        )


def visit_binary_operator_expression(
    expression_ast, compiled_module, var_namer, spaces
):
    str_spaces = " " * spaces

    left_expression = expression_ast.get_lhs_exp()
    visit_expression(left_expression, compiled_module, var_namer, spaces)
    lhs_exp = var_namer.pop()

    right_expression = expression_ast.get_rhs_exp()
    visit_expression(right_expression, compiled_module, var_namer, spaces)
    rhs_exp = var_namer.pop()

    operator_token = expression_ast.get_name()

    lhs_name = lhs_exp
    rhs_name = rhs_exp
    temp = var_namer.get_next_temp_var_name()
    compiled_module.append(
        f"{str_spaces}{temp} = {lhs_name} {operator_token.literal} {rhs_name}"
    )
    var_namer.push(temp)


def visit_prefix_expression(expression_ast, compiled_module, var_namer, spaces):
    str_spaces = " " * spaces

    rhs_expression = expression_ast.get_rhs_exp()
    visit_expression(rhs_expression, compiled_module, var_namer, spaces)
    rhs_exp = var_namer.pop()

    operator_token = expression_ast.get_name()

    rhs_name = rhs_exp
    temp = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp} = {operator_token.literal} {rhs_name}")
    var_namer.push(temp)


def visit_function_call_expression(expression_ast, compiled_module, var_namer, spaces):
    str_spaces = " " * spaces

    fn_name_exp = expression_ast.get_name()
    fn_name_token = fn_name_exp.get_name()
    # visit_expression(fn_name_exp, compiled_module, var_namer, spaces)
    # fn_name = var_namer.pop()
    arg_name_list = []
    argument_list = expression_ast.get_argument_list()
    for argument in argument_list:
        visit_expression(argument, compiled_module, var_namer, spaces)
        # visit_argument_list(argument_list, compiled_module, var_namer, spaces)
        arg = var_namer.pop()
        arg_name_list.append(arg)

    temp = var_namer.get_next_temp_var_name()
    arg_str = ", ".join(arg_name_list)
    compiled_module.append(f"{str_spaces}{temp} = {fn_name_token.literal}({arg_str})")
    var_namer.push(temp)


def visit_collection_expression(expression_ast, compiled_module, var_namer, spaces):
    if (
        expression_ast.left_type == LEFT_BRACKET
        and expression_ast.rhs_type == RIGHT_BRACKET
    ):
        visit_list_expression(expression_ast, compiled_module, var_namer, spaces)
    elif (
        expression_ast.left_type == LEFT_BRACE
        and expression_ast.rhs_type == RIGHT_BRACE
    ):
        visit_hash_expression(expression_ast, compiled_module, var_namer, spaces)
    else:
        raise Exception(
            f"Unknown collection type: {expression_ast.left_type} {expression_ast.rhs_type}"
        )


def visit_list_expression(expression_ast, compiled_module, var_namer, spaces):
    str_spaces = " " * spaces
    expression_array = expression_ast.get_collection_elements()
    temp = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp} = NEW_LIST")
    for expression in expression_array:
        visit_expression(expression, compiled_module, var_namer, spaces)
        element = var_namer.pop()
        compiled_module.append(f"{str_spaces}{temp} = {temp} APPEND {element}")
    var_namer.push(temp)


def visit_hash_expression(expression_ast, compiled_module, var_namer, spaces):
    if check_for_map_delimiter(expression_ast):
        visit_dict_expression(expression_ast, compiled_module, var_namer, spaces)
    else:
        visit_set_expression(expression_ast, compiled_module, var_namer, spaces)


def visit_dict_expression(expression_ast, compiled_module, var_namer, spaces):
    str_spaces = " " * spaces

    expression_array = expression_ast.get_collection_elements()
    temp = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp} = NEW_MAP")
    for expression in expression_array:
        key = expression.get_lhs_exp()
        value = expression.get_rhs_exp()
        visit_expression(key, compiled_module, var_namer, spaces)
        key_temp_name = var_namer.pop()
        visit_expression(value, compiled_module, var_namer, spaces)
        value_temp_name = var_namer.pop()
        compiled_module.append(
            f"{str_spaces}{temp} = {temp} SET_KEY {key_temp_name} TO {value_temp_name}"
        )
    var_namer.push(temp)


def visit_set_expression(expression_ast, compiled_module, var_namer, spaces):
    str_spaces = " " * spaces

    expression_array = expression_ast.get_collection_elements()
    temp = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp} = NEW_SET")
    for expression in expression_array:
        visit_expression(expression, compiled_module, var_namer, spaces)
        element = var_namer.pop()
        compiled_module.append(f"{str_spaces}{temp} = {temp} ADD {element}")
    var_namer.push(temp)


def check_for_map_delimiter(expression_ast):
    item_zero = expression_ast.get_collection_elements()[0]
    if str(item_zero.__class__.__name__) != "OperatorExpression":
        return False
    if item_zero.get_name().get_type() == COLON:
        return True


def visit_collection_access_expression(
    expression_ast, compiled_module, var_namer, spaces
):
    str_spaces = " " * spaces
    collection_name_exp = expression_ast.get_name()
    name_token = collection_name_exp.get_name()
    args = expression_ast.get_argument_list()
    arg_name_list = []
    if len(args) != 1:
        raise Exception("Only one argument is supported for collection access")
    for arg in args:
        visit_expression(arg, compiled_module, var_namer, spaces)

        arg_name = var_namer.pop()
        arg_name_list.append(arg_name)
    temp = var_namer.get_next_temp_var_name()
    compiled_module.append(
        f"{str_spaces}{temp} = {name_token.literal}[{','.join(arg_name_list)}]"
    )
    var_namer.push(temp)


def visit_method_call_or_field_expression(
    expression_ast, compiled_module, var_namer, spaces
):
    str_spaces = " " * spaces
    struct_name_exp = expression_ast.get_lhs_exp()
    struct_name_token = struct_name_exp.get_name()
    field_or_method_list = expression_ast.get_field_or_methods()

    var_namer.push(struct_name_token.literal)

    for field_or_method in field_or_method_list:

        if str(field_or_method.__class__.__name__) == "NameExpression":
            parent_name = var_namer.pop()
            temp = var_namer.get_next_temp_var_name()
            compiled_module.append(
                f"{str_spaces}{temp} = {parent_name}.{field_or_method.get_name().literal}"
            )
            var_namer.push(temp)

        elif str(field_or_method.__class__.__name__) == "FunctionCallExpression":
            parent_name = var_namer.pop()

            fn_name_exp = field_or_method.get_name()
            fn_name_token = fn_name_exp.get_name()

            arg_name_list = []
            argument_list = field_or_method.get_argument_list()
            for argument in argument_list:
                visit_expression(argument, compiled_module, var_namer, spaces)
                arg = var_namer.pop()
                arg_name_list.append(arg)

            temp = var_namer.get_next_temp_var_name()
            arg_str = ", ".join(arg_name_list)
            compiled_module.append(
                f"{str_spaces}{temp} = {parent_name}.{fn_name_token.literal}({arg_str})"
            )
            var_namer.push(temp)
        else:
            raise Exception(
                f"Unknown field or method type: {field_or_method.__class__.__name__}"
            )
