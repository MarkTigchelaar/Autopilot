from .compile_expressions import visit_expression
from symbols import IDENTIFIER

class TempVarNamer:
    def __init__(self, user_defined_variables):
        self.temp_var_count = 0
        self.user_defined_variables = set(user_defined_variables)
        self.labels = []
        self.label_id = 0

        self.loop_start_labels = []
        self.loop_end_labels = []

        self.stack = []

    def push(self, lhs):
        self.stack.append(lhs)

    def pop(self):
        return self.stack.pop()

    def get_next_temp_var_name(self):
        temp_var_name = f"temp{self.temp_var_count}"
        while temp_var_name in self.user_defined_variables:
            self.temp_var_count += 1
            temp_var_name = f"temp{self.temp_var_count}"
        self.user_defined_variables.add(temp_var_name)
        return temp_var_name

    def get_next_label(self):
        label = f"label{self.label_id}"
        self.label_id += 1
        self.labels.append(label)
        return label

    def get_last_label(self):
        return self.labels[-1]

    def pop_label(self):
        self.labels.pop()

    def add_loop_start_label(self, loop_name):
        self.loop_start_labels.append(loop_name)

    def pop_loop_start_label(self):
        self.loop_start_labels.pop()

    def get_inner_most_loop_start_label(self):
        return self.loop_start_labels[-1]

    def add_loop_end_label(self, loop_end_label):
        self.loop_end_labels.append(loop_end_label)

    def pop_loop_end_label(self):
        self.loop_end_labels.pop

    def get_inner_most_loop_end_label(self):
        return self.loop_end_labels[-1]


def compile_statements(statement_list, compiled_module, spaces):
    str_spaces = " " * spaces
    compiled_module.append(f"{str_spaces}BEGIN")

    str_spaces = " " * (spaces + 4)

    # gather all delarations, and map renames to avoid collisions
    declarations = get_declarations(statement_list)
    unioned_declations = remove_unneeded_declarations(declarations)
    user_def_var_names = set()
    for unioned_declation in unioned_declations:
        compiled_module.append(
            f"{str_spaces}DECLARE {unioned_declation.var_name} AS {unioned_declation.type_union_str}"
        )
        user_def_var_names.add(unioned_declation.var_name)
    var_namer = TempVarNamer(user_def_var_names)
    visit_statements(statement_list, compiled_module, var_namer, spaces + 4)


def get_declarations(statement_list):
    declarations = []
    for statement in statement_list:
        if str(statement.__class__.__name__) == "AssignmentStatement":
            declarations.append(statement)
        elif str(statement.__class__.__name__) in ("IfStatement", "ElifStatement"):
            add_option_type_declaration(statement, declarations)

        elif str(statement.__class__.__name__) == "ForStatement":
            add_for_loop_declarations(statement, declarations)
        if statement.has_next_statement_in_block():
            declarations.extend(
                get_declarations([statement.get_next_statement_in_block()])
            )
        if statement.has_nested_statements():
            declarations.extend(get_declarations(statement.get_statements()))
    return declarations

class TempDeclaration:
    def __init__(self, var_name, type):
        self.var_name = var_name
        self.type = type
    
    def get_name(self):
        return self.var_name
    
    def get_type(self):
        return self.type

class TokenPatch:
    def __init__(self, token):
        self.token = token
        self.literal = IDENTIFIER

    def get_type(self):
        return IDENTIFIER

def add_option_type_declaration(statement, declarations):
    if statement.is_option_type():
        unwrapped_optional_variable_name = statement.get_variable_name()
        #optional_variable_name = statement.get_optional_name().literal
        declarations.append(
            TempDeclaration(
                unwrapped_optional_variable_name, TokenPatch(unwrapped_optional_variable_name)
            )
        )

def add_for_loop_declarations(statement, declarations):
    if statement.is_optional_type():
        unwrapped_optional_variable_name = statement.get_unwrapped_optional_variable_name()
        declarations.append(
            TempDeclaration(
                unwrapped_optional_variable_name, TokenPatch(unwrapped_optional_variable_name)
            )
        )
    elif statement.is_collection_iteration():
        if statement.get_map_value_name() is not None:
            declarations.append(
                TempDeclaration(
                    statement.get_map_value_name(), TokenPatch(statement.get_map_value_name())
                )
            )
        declarations.append(
            TempDeclaration(
                statement.get_index_or_key_name(), TokenPatch(statement.get_index_or_key_name())
            )
        )
    # Otherwise, there is not declarations to add
    
def remove_unneeded_declarations(declarations):
    name_conflict_catalog = dict()

    for declaration in declarations:
        for other_declaration in declarations:
            if (
                declaration.get_name().literal == other_declaration.get_name().literal
                and declaration != other_declaration
            ):
                if declaration.get_name().literal not in name_conflict_catalog:
                    name_conflict_catalog[declaration.get_name().literal] = []
                name_conflict_catalog[declaration.get_name().literal].extend(
                    [
                        declaration.get_type().literal,
                        other_declaration.get_type().literal,
                    ]
                )

    # Pick the type with the biggest space available
    # local semantic checks weed out any situations where expressions might step over needed values in that memory slot
    unioned_declarations = []
    for name_conflict in name_conflict_catalog:
        declarations_to_remove = list(set(name_conflict_catalog[name_conflict]))
        type_union_str = ""
        for declaration in declarations_to_remove:
            type_union_str += declaration + "|"
        type_union_str = type_union_str[:-1]
        unioned_declarations.append(UnionedDeclaration(name_conflict, type_union_str))
    normal_declarations = []
    for declaration in declarations:
        if declaration.get_name().literal not in name_conflict_catalog:
            normal_declarations.append(
                UnionedDeclaration(
                    declaration.get_name().literal, declaration.get_type().literal
                )
            )
    normal_declarations.extend(unioned_declarations)
    return normal_declarations


class UnionedDeclaration:
    def __init__(self, var_name, type_union_str):
        self.var_name = var_name
        self.type_union_str = type_union_str


def visit_statements(statement_list, compiled_module, var_namer, spaces):
    str_spaces = " " * spaces
    defer_statements = []
    for statement in statement_list:
        if str(statement.__class__.__name__) == "DeferStatement":
            defer_statements.append(statement)
    for statement in statement_list:
        if str(statement.__class__.__name__) == "AssignmentStatement":
            visit_assignment_statement(statement, compiled_module, var_namer, spaces)
        if str(statement.__class__.__name__) == "IfStatement":
            block_end_label = var_namer.get_next_label()
            if statement.has_next_statement_in_block():
                next_block_label = var_namer.get_next_label()
            else:
                next_block_label = block_end_label
            visit_if_statement(
                statement,
                compiled_module,
                var_namer,
                spaces,
                next_block_label=next_block_label,
                block_end_label=block_end_label,
            )
            compiled_module.append(f"{str_spaces}LABEL {block_end_label}:")
        if str(statement.__class__.__name__) == "UnlessStatement":
            block_end_label = var_namer.get_next_label()
            visit_unless_statement(
                statement,
                compiled_module,
                var_namer,
                spaces,
                block_end_label=block_end_label,
            )

        if str(statement.__class__.__name__) == "ForStatement":
            visit_for_statement(statement, compiled_module, var_namer, spaces)
        if str(statement.__class__.__name__) == "WhileStatement":
            visit_while_statement(statement, compiled_module, var_namer, spaces)
        if str(statement.__class__.__name__) == "LoopStatement":
            visit_loop_statement(statement, compiled_module, var_namer, spaces)
        if str(statement.__class__.__name__) == "BreakStatement":
            visit_break_statement(statement, compiled_module, var_namer, spaces)
        if str(statement.__class__.__name__) == "ContinueStatement":
            visit_continue_statement(statement, compiled_module, var_namer, spaces)
        if str(statement.__class__.__name__) == "SwitchStatement":
            visit_switch_statement(statement, compiled_module, var_namer, spaces)
        if str(statement.__class__.__name__) == "ReturnStatement":
            for defer_statement in defer_statements:
                visit_defer_statement(
                    defer_statement, compiled_module, var_namer, spaces
                )
            visit_return_statement(statement, compiled_module, var_namer, spaces)
        if str(statement.__class__.__name__) == "DeferStatement":
            continue
        if str(statement.__class__.__name__) == "ReassignmentOrMethodCall":
            visit_reassign_or_method_call(statement, compiled_module, var_namer, spaces)


def visit_assignment_statement(statement, compiled_module, var_namer, spaces):
    expression_ast = statement.get_expression_ast()
    visit_expression(expression_ast, compiled_module, var_namer, spaces)
    str_spaces = " " * spaces
    var_name = statement.get_name().literal
    expression = var_namer.pop()
    compiled_module.append(f"{str_spaces}{var_name} = {expression}")


def visit_if_statement(
    statement, compiled_module, var_namer, spaces, next_block_label, block_end_label
):
    str_spaces = " " * spaces
    if statement.is_option_type():
        visit_option_type_test_condition(
            statement, compiled_module, var_namer, spaces, next_block_label
        )
    else:
        visit_test_condition(
            statement, compiled_module, var_namer, spaces, next_block_label
        )
    visit_statements(statement.get_statements(), compiled_module, var_namer, spaces)
    compiled_module.append(f"{str_spaces}GOTO {block_end_label}")
    if statement.has_next_statement_in_block():
        if (
            str(statement.get_next_statement_in_block().__class__.__name__)
            == "ElifStatement"
        ):
            compiled_module.append(f"{str_spaces}LABEL {next_block_label}:")
            if statement.get_next_statement_in_block().has_next_statement_in_block():
                nested_next_block_label = var_namer.get_next_label()
            else:
                nested_next_block_label = block_end_label
            visit_if_statement(
                statement.get_next_statement_in_block(),
                compiled_module,
                var_namer,
                spaces,
                next_block_label=nested_next_block_label,
                block_end_label=block_end_label,
            )
            # compiled_module.append(f"{str_spaces}GOTO {var_namer.get_last_label()}")
        elif (
            str(statement.get_next_statement_in_block().__class__.__name__)
            == "ElseStatement"
        ):
            else_statement = statement.get_next_statement_in_block()
            visit_statements(
                else_statement.get_statements(), compiled_module, var_namer, spaces
            )
            # visit_else_statement(statement.get_next_statement_in_block(), compiled_module, var_namer, spaces)
        else:
            raise Exception(
                f"Unknown statement type: {statement.get_next_statement_in_block().__class__.__name__}"
            )


def visit_unless_statement(
    statement, compiled_module, var_namer, spaces, block_end_label
):
    str_spaces = " " * spaces
    visit_test_condition(
        statement,
        compiled_module,
        var_namer,
        spaces,
        block_end_label,
        jump_if_false=False,
    )
    visit_statements(statement.get_statements(), compiled_module, var_namer, spaces)
    compiled_module.append(f"{str_spaces}LABEL {block_end_label}:")


def visit_test_condition(
    statement, compiled_module, var_namer, spaces, next_block_label, jump_if_false=True
):
    expression_ast = statement.get_expression_ast()
    visit_expression(expression_ast, compiled_module, var_namer, spaces)
    str_spaces = " " * spaces
    boolean_variable = var_namer.pop()
    # This is because jump to block after (el)if statement happens if condition is false, not if it is true
    conditional = "IF_FALSE" if jump_if_false else "IF_TRUE"
    compiled_module.append(
        f"{str_spaces}{conditional} {boolean_variable} GOTO {next_block_label}"
    )


# make helper functions for ifs / for loops
def visit_option_type_test_condition(
    statement, compiled_module, var_namer, spaces, next_block_label
):
    str_spaces = " " * spaces
    unwrapped_optional_variable_name = statement.get_variable_name().literal
    optional_variable_name = statement.get_optional_name().literal
    temp = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp} = {optional_variable_name}.tag")
    compiled_module.append(f"{str_spaces}IF_FALSE {temp} GOTO {next_block_label}")
    compiled_module.append(
        f"{str_spaces}{unwrapped_optional_variable_name} = {optional_variable_name}.value"
    )

    # compiled_module.append(f"{str_spaces}LABEL {block_end_label}:")


def visit_break_statement(statement, compiled_module, var_namer, spaces):
    str_spaces = " " * spaces
    block_end_label = var_namer.get_inner_most_loop_end_label()
    label_token = statement.get_label_name()
    if label_token:
        compiled_module.append(f"{str_spaces}GOTO {label_token.literal}")
    else:
        compiled_module.append(f"{str_spaces}GOTO {block_end_label}")


def visit_continue_statement(statement, compiled_module, var_namer, spaces):
    str_spaces = " " * spaces
    block_start_label = var_namer.get_inner_most_loop_start_label()
    compiled_module.append(f"{str_spaces}GOTO {block_start_label}")


def visit_while_statement(statement, compiled_module, var_namer, spaces):
    str_spaces = " " * spaces
    loop_name_token = statement.get_loop_name()
    block_start_label = var_namer.get_next_label()
    if loop_name_token:
        block_end_label = loop_name_token.literal
    else:
        block_end_label = var_namer.get_next_label()
    var_namer.add_loop_start_label(block_start_label)
    var_namer.add_loop_end_label(block_end_label)
    compiled_module.append(f"{str_spaces}LABEL {block_start_label}:")
    visit_while_statement_helper(
        statement, compiled_module, var_namer, spaces, block_end_label=block_end_label
    )
    compiled_module.append(f"{str_spaces}GOTO {block_start_label}")
    compiled_module.append(f"{str_spaces}LABEL {block_end_label}:")
    var_namer.pop_loop_start_label()
    var_namer.pop_loop_end_label()


def visit_while_statement_helper(
    statement, compiled_module, var_namer, spaces, block_end_label
):
    visit_test_condition(statement, compiled_module, var_namer, spaces, block_end_label)
    visit_statements(statement.get_statements(), compiled_module, var_namer, spaces)


def visit_loop_statement(statement, compiled_module, var_namer, spaces):
    str_spaces = " " * spaces
    loop_name_token = statement.get_loop_name()
    block_start_label = var_namer.get_next_label()
    if loop_name_token:
        block_end_label = loop_name_token.literal
    else:
        block_end_label = var_namer.get_next_label()
    var_namer.add_loop_start_label(block_start_label)
    var_namer.add_loop_end_label(block_end_label)
    compiled_module.append(f"{str_spaces}LABEL {block_start_label}:")
    visit_statements(statement.get_statements(), compiled_module, var_namer, spaces)
    compiled_module.append(f"{str_spaces}GOTO {block_start_label}")
    compiled_module.append(f"{str_spaces}LABEL {block_end_label}:")
    var_namer.pop_loop_start_label()
    var_namer.pop_loop_end_label()


def visit_return_statement(statement, compiled_module, var_namer, spaces):
    str_spaces = " " * spaces
    expression_ast = statement.get_expression_ast()
    visit_expression(expression_ast, compiled_module, var_namer, spaces)
    expression = var_namer.pop()
    compiled_module.append(f"{str_spaces}RETURN {expression}")


def visit_switch_statement(statement, compiled_module, var_namer, spaces):
    str_spaces = " " * spaces
    test_expression = statement.get_test_expression()
    visit_expression(test_expression, compiled_module, var_namer, spaces)
    test_expression = var_namer.pop()

    case_statement_labels = []
    for case_statement in statement.get_statements():
        visit_case_statement_test_expression(
            case_statement,
            compiled_module,
            var_namer,
            spaces,
            test_expression,
            case_statement_labels,
        )

    block_end_label = var_namer.get_next_label()
    for i, case_statement in enumerate(statement.get_statements()):
        label = case_statement_labels[i]
        visit_case_statement(
            case_statement, compiled_module, var_namer, spaces, label, block_end_label
        )
    compiled_module.append(f"{str_spaces}LABEL {block_end_label}:")


def visit_case_statement_test_expression(
    case_statement,
    compiled_module,
    var_namer,
    spaces,
    test_expression,
    case_statement_labels,
):
    str_spaces = " " * spaces
    case_label = var_namer.get_next_label()
    case_statement_labels.append(case_label)
    for value_token in case_statement.get_values():
        # visit_expression(value, compiled_module, var_namer, spaces)
        # value = var_namer.pop()
        compiled_module.append(
            f"{str_spaces}IF {test_expression} == {value_token.literal} GOTO {case_label}"
        )
    if len(case_statement.get_values()) == 0:
        compiled_module.append(f"{str_spaces}GOTO {case_label}")


def visit_case_statement(
    case_statement, compiled_module, var_namer, spaces, label, block_end_label
):
    str_spaces = " " * spaces
    compiled_module.append(f"{str_spaces}LABEL {label}:")
    visit_statements(
        case_statement.get_statements(), compiled_module, var_namer, spaces
    )
    compiled_module.append(f"{str_spaces}GOTO {block_end_label}")


def visit_for_statement(statement, compiled_module, var_namer, spaces):
    str_spaces = " " * spaces
    loop_name_token = statement.get_loop_name()
    block_start_label = var_namer.get_next_label()
    if loop_name_token:
        block_end_label = loop_name_token.literal
    else:
        block_end_label = var_namer.get_next_label()
    var_namer.add_loop_start_label(block_start_label)
    var_namer.add_loop_end_label(block_end_label)
    visit_for_statement_helper(
        statement,
        compiled_module,
        var_namer,
        spaces,
        block_start_label,
        block_end_label=block_end_label,
    )
    compiled_module.append(f"{str_spaces}LABEL {block_end_label}:")
    var_namer.pop_loop_start_label()
    var_namer.pop_loop_end_label()


def visit_for_statement_helper(
    statement, compiled_module, var_namer, spaces, block_start_label, block_end_label
):
    str_spaces = " " * spaces

    if statement.is_optional_type():

        visit_for_statement_optional_type(
            statement,
            compiled_module,
            var_namer,
            spaces,
            block_start_label,
            block_end_label,
        )
    elif statement.is_collection_iteration():
        visit_for_statement_collection(
            statement,
            compiled_module,
            var_namer,
            spaces,
            block_start_label,
            block_end_label,
        )
    else:
        visit_for_statement_range(
            statement,
            compiled_module,
            var_namer,
            spaces,
            block_start_label,
            block_end_label,
        )
    compiled_module.append(f"{str_spaces}GOTO {block_start_label}")
    # compiled_module.append(f"{str_spaces}LABEL {block_end_label}:")


"""
    The following was auto generated, check logic and test
"""


# for let a in collection do
def visit_for_statement_optional_type(
    statement, compiled_module, var_namer, spaces, block_start_label, block_end_label
):
    str_spaces = " " * spaces
    unwrapped_optional_variable_name = (
        statement.get_unwrapped_optional_variable_name().literal
    )
    optional_variable_name = statement.get_optional_variable_name().literal

    temp = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp} = {optional_variable_name}.length")
    temp1 = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp1} = 0")
    compiled_module.append(f"{str_spaces}LABEL {block_start_label}:")

    temp2 = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp2} = {temp1} < {temp}")
    compiled_module.append(f"{str_spaces}IF_FALSE {temp2} GOTO {block_end_label}")
    temp3 = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp3} = {optional_variable_name}[{temp1}]")
    temp4 = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp4} = {temp3}.tag")
    unwrapped_label = var_namer.get_next_label()
    compiled_module.append(f"{str_spaces}IF_TRUE {temp4} GOTO {unwrapped_label}")
    compiled_module.append(f"{str_spaces}{temp1} = {temp1} + 1")
    compiled_module.append(f"{str_spaces}GOTO {block_start_label}")
    compiled_module.append(f"{str_spaces}LABEL {unwrapped_label}:")
    compiled_module.append(
        f"{str_spaces}{unwrapped_optional_variable_name} = {optional_variable_name}.value"
    )
    visit_statements(statement.get_statements(), compiled_module, var_namer, spaces)
    compiled_module.append(f"{str_spaces}{temp1} = {temp1} + 1")


# for i in collection
# for key, value in collection
def visit_for_statement_collection(
    statement, compiled_module, var_namer, spaces, block_start_label, block_end_label
):
    if statement.get_map_value_name() is not None:
        visit_for_statement_map(
            statement,
            compiled_module,
            var_namer,
            spaces,
            block_start_label,
            block_end_label,
        )
    else:
        visit_for_statement_list(
            statement,
            compiled_module,
            var_namer,
            spaces,
            block_start_label,
            block_end_label,
        )


def visit_for_statement_list(
    statement, compiled_module, var_namer, spaces, block_start_label, block_end_label
):
    str_spaces = " " * spaces
    collection_name = statement.get_collection_name().literal
    temp = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp} = {collection_name}.length")
    temp1 = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp1} = 0")
    compiled_module.append(f"{str_spaces}LABEL {block_start_label}:")
    temp2 = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp2} = {temp1} < {temp}")
    compiled_module.append(f"{str_spaces}IF_FALSE {temp2} GOTO {block_end_label}")
    key_or_var_name = statement.get_index_or_key_name().literal
    compiled_module.append(
        f"{str_spaces}{key_or_var_name} = {collection_name}[{temp1}]"
    )

    visit_statements(statement.get_statements(), compiled_module, var_namer, spaces)
    compiled_module.append(f"{str_spaces}{temp1} = {temp1} + 1")


def visit_for_statement_map(
    statement, compiled_module, var_namer, spaces, block_start_label, block_end_label
):
    str_spaces = " " * spaces
    collection_name = statement.get_collection_name().literal
    keys_ref = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{keys_ref} = {collection_name}.keys")
    temp1 = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp1} = {keys_ref}.length")
    temp2 = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp2} = 0")
    compiled_module.append(f"{str_spaces}LABEL {block_start_label}:")
    temp3 = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp3} = {temp2} < {temp1}")
    compiled_module.append(f"{str_spaces}IF_FALSE {temp3} GOTO {block_end_label}")
    key_var_name = statement.get_index_or_key_name().literal
    value_literal = statement.get_map_value_name().literal
    compiled_module.append(f"{str_spaces}{key_var_name} = {keys_ref}[{temp2}]")
    compiled_module.append(
        f"{str_spaces}{value_literal} = {collection_name}[{key_var_name}]"
    )
    visit_statements(statement.get_statements(), compiled_module, var_namer, spaces)
    compiled_module.append(f"{str_spaces}{temp2} = {temp2} + 1")


# for i in 1..10, 2 as loop do
def visit_for_statement_range(
    statement, compiled_module, var_namer, spaces, block_start_label, block_end_label
):
    str_spaces = " " * spaces
    index_start_value = statement.get_index_start_name().literal
    index_stop_value = statement.get_index_stop_name().literal
    iteration_step_size = 1
    if statement.get_iteration_step_size():
        iteration_step_size = statement.get_iteration_step_size().literal
    start_index_var = var_namer.get_next_temp_var_name()
    stop_index_var = var_namer.get_next_temp_var_name()
    step_var = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{start_index_var} = {index_start_value}")
    compiled_module.append(f"{str_spaces}{stop_index_var} = {index_stop_value}")
    compiled_module.append(f"{str_spaces}{step_var} = {iteration_step_size}")
    compiled_module.append(f"{str_spaces}LABEL {block_start_label}:")
    temp = var_namer.get_next_temp_var_name()
    compiled_module.append(f"{str_spaces}{temp} = {start_index_var} < {stop_index_var}")
    compiled_module.append(f"{str_spaces}IF_FALSE {temp} GOTO {block_end_label}")
    visit_statements(statement.get_statements(), compiled_module, var_namer, spaces)
    compiled_module.append(
        f"{str_spaces}{start_index_var} = {start_index_var} + {step_var}"
    )


def visit_defer_statement(defer_statement, compiled_module, var_namer, spaces):
    if defer_statement.method_call is None:
        raise Exception("Defer statement has no method call")
    # defer statements do not involve assignment, just a call to a method or function
    visit_reassign_or_method_call(
        defer_statement.method_call, compiled_module, var_namer, spaces
    )


def visit_reassign_or_method_call(statement, compiled_module, var_namer, spaces):
    l_value_exp = statement.l_value_exp
    r_value_exp = statement.r_value_exp
    str_spaces = " " * spaces
    if statement.get_assignment_token():
        visit_expression(l_value_exp, compiled_module, var_namer, spaces)
        l_value = var_namer.pop()
        visit_expression(r_value_exp, compiled_module, var_namer, spaces)
        r_value = var_namer.pop()
        proess_re_assignment_by_type(
            statement, compiled_module, spaces, l_value, r_value
        )
    else:
        if r_value_exp is not None:
            raise Exception(f"R VALUE IS NOT NONE: {r_value_exp}")
        visit_expression(l_value_exp, compiled_module, var_namer, spaces)
        compiled_module[-1] = str_spaces + compiled_module[-1].split(" = ")[1]
        _ = var_namer.pop()


def proess_re_assignment_by_type(statement, compiled_module, spaces, l_value, r_value):
    str_spaces = " " * spaces
    descriptor = statement.get_assignment_token().literal
    if descriptor == "^=":
        compiled_module.append(f"{str_spaces}{l_value} = {l_value} ^ {r_value}")
    elif descriptor == "+=":
        compiled_module.append(f"{str_spaces}{l_value} = {l_value} + {r_value}")
    elif descriptor == "-=":
        compiled_module.append(f"{str_spaces}{l_value} = {l_value} - {r_value}")
    elif descriptor == "*=":
        compiled_module.append(f"{str_spaces}{l_value} = {l_value} * {r_value}")
    elif descriptor == "/=":
        compiled_module.append(f"{str_spaces}{l_value} = {l_value} / {r_value}")
    elif descriptor == "%=":
        compiled_module.append(f"{str_spaces}{l_value} = {l_value} % {r_value}")
    elif descriptor == "=":
        compiled_module.append(f"{str_spaces}{l_value} = {r_value}")
    else:
        raise Exception(f"Unknown descriptor: {descriptor}")
