from CodeGeneration.APIntermediateLanguage.process_ap_ast_to_ir import compile_to_ap_bytecode
from CodeGeneration.PythonGenerator.generate_python_code import generate_python_code
from CodeGeneration.APIntermediateLanguage.compile_enums import find_general_type, process_enum_fields
from keywords import is_primitive_type
class RenamedCodeBlock:
    def __init__(self):
        self.key_value_defines = []
        self.linear_type_defines = []
        self.failable_type_defines = []
        self.function_type_defines = []
        self.enums = []
        self.errors = []
        self.interfaces = []
        self.unions = []
        self.structs = []
        self.functions = []
        self.unit_tests = []
        self.built_in_libs = None

def generate_code(raw_module_collection, output_file, language_name):
    merged_code = merge_modules(raw_module_collection)
    match language_name:
        case "python":

            generate_python_code(merged_code, output_file)
        case _:
            compile_to_ap_bytecode(raw_module_collection, output_file)


def merge_modules(raw_module_collection):
    code_blocks = RenamedCodeBlock()
    for raw_module in raw_module_collection.get_raw_modules():
        #print("raw_module")
        rename_module_components(raw_module, code_blocks)

    
    select_built_in_libs(code_blocks, raw_module_collection)
    return code_blocks


def rename_module_components(raw_module, code_blocks):
    for define_statement in raw_module.key_value_defines:
        renamed_object = rename_kv_define(raw_module, define_statement)
        code_blocks.key_value_defines.append(renamed_object)
    for define_statement in raw_module.linear_type_defines:
        renamed_object = rename_linear_type_defines(raw_module, define_statement)
        code_blocks.linear_type_defines.append(renamed_object)
    for define_statement in raw_module.failable_type_defines:
        renamed_object = rename_failable_type_defines(raw_module, define_statement)
        code_blocks.failable_type_defines.append(renamed_object)
    for define_statement in raw_module.function_type_defines:
        renamed_object = rename_failable_type_defines(raw_module, define_statement)
        code_blocks.function_type_defines.append(renamed_object)
    for enum_statement in raw_module.enums:
        enum_statement = rename_enums(raw_module, enum_statement)
        code_blocks.enums.append(enum_statement)
    for error_statement in raw_module.errors:
        error_statement = rename_errors(raw_module, error_statement)
        code_blocks.errors.append(error_statement)
    for union_statement in raw_module.unions:
        union_statement = rename_unions(raw_module, union_statement)
        code_blocks.unions.append(union_statement)
    for interface_statement in raw_module.interfaces:
        interface_statement = rename_interfaces(raw_module, interface_statement)
        code_blocks.interfaces.append(interface_statement)
    for function_statement in raw_module.functions:
        function_statement = rename_functions(raw_module, function_statement)
        code_blocks.functions.append(function_statement)
    for struct_statement in raw_module.structs:
        struct_statement = rename_structs(raw_module, struct_statement)
        code_blocks.structs.append(struct_statement)

    # for unittest_statement in raw_module.unit_tests:
    #     unittest_statement.rename_module_components(raw_module.name)

def rename_token_literals(raw_module, token):
    if is_primitive_type(token, True):
        return
    is_imported = False
    for import_statement in raw_module.imports:
        other_module_name = import_statement.path_list[-1].node_token.literal
        for import_item in import_statement.import_list:
            if token.literal == import_item.name_token.literal:
                if import_statement.import_type == "library":
                    map_to_built_in_libs(token, import_statement, raw_module)
                else:
                    token.literal = other_module_name + "_" + token.literal
                is_imported = True
                break
        if is_imported:
            break
    if is_imported:
        return
        #raise Exception("Descriptor not found in import statement")
    token.literal = raw_module.name + "_" + token.literal

def rename_kv_define(raw_module, kv_define_statement):
    kv_define_statement.descriptor_token.literal = raw_module.name + "_" + kv_define_statement.descriptor_token.literal
    key_type_token = kv_define_statement.sub_type.get_key_token()
    rename_token_literals(raw_module, key_type_token)
    value_type_token = kv_define_statement.sub_type.get_value_token()
    rename_token_literals(raw_module, value_type_token)
    return kv_define_statement




def descriptor_vs_define_new_name(kv_define_statement, import_item, other_module_name):
    name_token = import_item.new_name_token
    if name_token is None:
        name_token = import_item.name_token
    if kv_define_statement.descriptor_token.literal == name_token.literal:
        kv_define_statement.descriptor_token.literal = other_module_name + "_" + kv_define_statement.descriptor_token.literal
        return True
    return False

def descriptor_vs_enum_name(enum_statement, import_item, other_module_name):
    name_token = import_item.new_name_token
    if name_token is None:
        name_token = import_item.name_token
    if enum_statement.name_token.literal == name_token.literal:
        enum_statement.name_token.literal = other_module_name + "_" + enum_statement.name_token.literal
        return True
    return False

def rename_linear_type_defines(raw_module, define_statement):
    define_statement.descriptor_token.literal = raw_module.name + "_" + define_statement.descriptor_token.literal
    element_type_token = define_statement.sub_type.get_value_token()
    rename_token_literals(raw_module, element_type_token)
    return define_statement


def rename_failable_type_defines(raw_module, define_statement):
    define_statement.descriptor_token.literal = raw_module.name + "_" + define_statement.descriptor_token.literal
    element_type_token = define_statement.sub_type.get_value_token()
    rename_token_literals(raw_module, element_type_token)
    return define_statement

def rename_enums(raw_module, enum_statement):
    enum_statement.name_token.literal = raw_module.name + "_" + enum_statement.name_token.literal
    add_values_to_enum_items(enum_statement)
    return enum_statement

def add_values_to_enum_items(enum_statement):
    general_type = find_general_type(enum_statement)
    enum_fields = process_enum_fields(enum_statement, general_type)
    enum_statement.filled_in_items = enum_fields


def rename_errors(raw_module, error_statement):
    is_imported = False
    if is_imported:
        raise Exception("Descriptor not found in import statement")
    error_statement.name_token.literal = raw_module.name + "_" + error_statement.name_token.literal
    return error_statement

def rename_unions(raw_module, union_statement):
    union_statement.name_token.literal = raw_module.name + "_" + union_statement.name_token.literal
    for union_item in union_statement.items:
        rename_token_literals(raw_module, union_item.type_token)
    return union_statement


def rename_interfaces(raw_module, interface_statement):
    interface_statement.name_token.literal = raw_module.name + "_" + interface_statement.name_token.literal
    for header in interface_statement.fn_headers:
        if header.get_return_type() is not None:
            rename_token_literals(raw_module, header.get_return_type())
        for arg in header.get_args():
            rename_token_literals(raw_module, arg.arg_type_token)
    return interface_statement

def rename_functions(raw_module, function_statement):
    function_statement.header.name_token.literal = raw_module.name + "_" + function_statement.header.name_token.literal
    for args in function_statement.header.get_args():
        rename_token_literals(raw_module, args.arg_type_token)
    rename_function_variable_types(raw_module, function_statement)
    rename_expression_function_calls(raw_module, function_statement)
    return function_statement


def rename_structs(raw_module, struct_statement):
    for function in struct_statement.get_functions():
        for args in function.get_args():
            rename_token_literals(raw_module, args.arg_type_token)
        if function.get_header().get_return_type() is not None:
            rename_token_literals(raw_module, function.get_header().get_return_type())
        rename_function_variable_types(raw_module, function)
        rename_expression_function_calls(raw_module, function)
    for field in struct_statement.get_fields():
        rename_token_literals(raw_module, field.type_token)
    for interface in struct_statement.get_interfaces():
        rename_token_literals(raw_module, interface)
    struct_statement.name_token.literal = raw_module.name + "_" + struct_statement.name_token.literal
    return struct_statement


def rename_function_variable_types(raw_module, function):
    find_and_rename_declare_statement_types(raw_module, function.get_statements())
    find_and_rename_enum_switch_cases(raw_module, function.get_statements())


def find_and_rename_declare_statement_types(raw_module, statements):
    for statement in statements:
        if str(statement.__class__.__name__) == "AssignmentStatement":

            rename_token_literals(raw_module, statement.get_type())
        if statement.has_nested_statements():
            find_and_rename_declare_statement_types(raw_module, statement.get_statements())
        if statement.has_next_statement_in_block():
            find_and_rename_declare_statement_types(raw_module, [statement.get_next_statement_in_block()])

def find_and_rename_enum_switch_cases(raw_module, statements):
    for statement in statements:
        if str(statement.__class__.__name__) == "SwitchStatement":
            for case in statement.get_statements():
                if case.has_enum_references():
                    for enum in case.get_enum_references():
                        rename_token_literals(raw_module, enum.get_enum_name())
        
def rename_expression_function_calls(raw_module, function):
    find_and_rename_function_calls(raw_module, function.get_statements(), function.get_args())


def find_and_rename_function_calls(raw_module, statements, function_args):
    for statement in statements:
        if statement.has_nested_statements():
            find_and_rename_function_calls(raw_module, statement.get_statements(), function_args)
        if statement.has_next_statement_in_block():
            find_and_rename_function_calls(raw_module, [statement.get_next_statement_in_block()], function_args)
        # if str(statement.__class__.__name__) == "SwitchStatement":
        #     for case in statement.get_statements():
        #         find_and_rename_function_calls(raw_module, case.get_statements(), function_args)
        if str(statement.__class__.__name__) == "AssignmentStatement":
            if statement.get_expression_ast() is not None:
                find_and_rename_function_calls_in_expression(raw_module, statement.get_expression_ast(), function_args)
        if str(statement.__class__.__name__) == "ReassignmentOrMethodCall":
            if statement.r_value_exp is not None:
                find_and_rename_function_calls_in_expression(raw_module, statement.r_value_exp, function_args)
            elif statement.l_value_exp is not None:
                find_and_rename_function_calls_in_expression(raw_module, statement.l_value_exp, function_args)
        if str(statement.__class__.__name__) == "IfStatement":
            if statement.has_expression_ast():
                find_and_rename_function_calls_in_expression(raw_module, statement.get_expression_ast(), function_args)
        if str(statement.__class__.__name__) == "ElifStatement":
            if statement.has_expression_ast():
                find_and_rename_function_calls_in_expression(raw_module, statement.get_expression_ast(), function_args)
        if str(statement.__class__.__name__) == "UnlessStatement":
            if statement.has_expression_ast():
                find_and_rename_function_calls_in_expression(raw_module, statement.get_expression_ast(), function_args)
        if str(statement.__class__.__name__) == "WhileStatement":
            if statement.has_expression_ast():
                find_and_rename_function_calls_in_expression(raw_module, statement.get_expression_ast(), function_args)
        if str(statement.__class__.__name__) == "DeferStatement":
            reassignment_statement = statement.get_method_or_reassignment()
            find_and_rename_function_calls_in_expression(raw_module, reassignment_statement.l_value_exp, function_args)
        if str(statement.__class__.__name__) == "ReturnStatement":
            if statement.has_expression_ast():
                find_and_rename_function_calls_in_expression(raw_module, statement.get_expression_ast(), function_args)

def find_and_rename_function_calls_in_expression(raw_module, expression, function_args):
    if str(expression.__class__.__name__) == "FunctionCallExpression":
        rename_function_maybe(raw_module, expression, function_args)
        return
    if str(expression.__class__.__name__) == "CollectionAccessExpression":
        for arg_exp in expression.get_argument_list():
            find_and_rename_function_calls_in_expression(raw_module, arg_exp, function_args)
    elif str(expression.__class__.__name__) == "CollectionExpression":
        for exp in expression.get_collection_elements():
            find_and_rename_function_calls_in_expression(raw_module, exp, function_args)
    elif str(expression.__class__.__name__) == "PrefixExpression":
        find_and_rename_function_calls_in_expression(raw_module, expression.get_rhs_exp(), function_args)
    elif str(expression.__class__.__name__) == "OperatorExpression":
        find_and_rename_function_calls_in_expression(raw_module, expression.get_lhs_exp(), function_args)
        find_and_rename_function_calls_in_expression(raw_module, expression.get_rhs_exp(), function_args)


def rename_function_maybe(raw_module, expression, function_args):
    for arg in expression.get_argument_list():
        find_and_rename_function_calls_in_expression(raw_module, arg, function_args)
    for arg in function_args:
        if expression.get_name().get_name().literal == arg.arg_name_token.literal:
            # This means the functon name is the name of a function pointer passed into the caller function.
            return
    rename_token_literals(raw_module, expression.get_name().get_name())




def select_built_in_libs(code_blocks, raw_module_collection):
    builtin_libs = raw_module_collection.get_built_in_libs()
    imports = []#raw_module_collection.get_imports()
    for module in raw_module_collection.get_raw_modules():
        for import_statement in module.imports:
            if import_statement.import_type == "library":
                imports.append(import_statement)
    for import_statement in imports:
        lib_name = import_statement.path_list[-1].node_token.literal
        if lib_name in builtin_libs:
            code_blocks.built_in_libs.update(builtin_libs[lib_name])


    # code_blocks.built_in_libs


def map_to_built_in_libs(token, import_statement, raw_module):
    library = raw_module.get_built_in_libs()
    library_import_path = import_statement.path_list
    for i in range(len(library_import_path)):
        path_item = library_import_path[i]
        if path_item.node_token.literal in library:
            
            sub_modules = library[path_item.node_token.literal]["sub_modules"]
            if len(sub_modules) == 0 and i < len(library_import_path) - 1:
                raise Exception("sub module not found in built-in library")
            if len(sub_modules) == 0 and i == len(library_import_path) - 1:
                library = library[path_item.node_token.literal]
                break
            library = sub_modules
        else:
            raise Exception("Library not found in built-in library")
    
    if token.literal in library["functions"]: # key error here
        token.literal = library["functions"][token.literal]["target_name"]

    elif token.literal in library["enums"]:
        token.literal = library["enums"][token.literal]["target_name"]
    elif token.literal in library["classes"]:
        token.literal = library["classes"][token.literal]["target_name"]


            # if path_item.direction_token is not None:
            #     if path_item.direction_token.literal in library["sub_modules"]:
            #         library = library["sub_modules"][path_item.direction_token.literal]
            #     else:
            #         raise Exception("Library not found in built-in library")
            # if token.literal in library["functions"]:
            #     token.literal = library["functions"][token.literal]["target_name"]
            #     return
            # else:
            #     raise Exception("Function not found in built-in library")



    # if library_name in raw_module.get_built_in_libs():
    #     built_in_lib = raw_module.get_built_in_libs()[library_name]
    #     if token.literal in built_in_lib:
    #         token.literal = built_in_lib[token.literal]["target_name"]
    #         return
    # else:
    #     raise Exception(f"Library {library_name} not found in built-in library")