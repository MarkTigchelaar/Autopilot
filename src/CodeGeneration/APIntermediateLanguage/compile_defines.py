

def compile_defines(raw_module, compiled_module, symbol_table, spaces):
    str_spaces = " " * spaces
    for define in raw_module.linear_type_defines:
        compiled_module.append(f"{str_spaces}DEFINE {define.sub_type.get_type().literal} {define.get_definition().literal}")
        compiled_module.append(f"{str_spaces}{str_spaces}VALUE_TYPE {define.sub_type.get_value_token().literal}")
        compiled_module.append(f"{str_spaces}END {define.sub_type.get_type().literal} {define.get_definition().literal}")

    for define in raw_module.key_value_defines:
        compiled_module.append(f"{str_spaces}DEFINE {define.sub_type.get_type().literal} {define.get_definition().literal}")
        compiled_module.append(f"{str_spaces}{str_spaces}KEY_TYPE {define.sub_type.get_key_token().literal}")
        compiled_module.append(f"{str_spaces}{str_spaces}VALUE_TYPE {define.sub_type.get_value_token().literal}")
        compiled_module.append(f"{str_spaces}END {define.sub_type.get_type().literal} {define.get_definition().literal}")

    for define in raw_module.failable_type_defines:
        compiled_module.append(f"{str_spaces}DEFINE {define.sub_type.get_type().literal} {define.get_descriptor_token().literal}")
        compiled_module.append(f"{str_spaces}{str_spaces}VALUE_TYPE {define.sub_type.get_value_token().literal}")
        error_token = define.sub_type.get_error_token()
        if error_token is not None:
            compiled_module.append(f"{str_spaces}{str_spaces}ERROR_TYPE {error_token.literal}")
        compiled_module.append(f"{str_spaces}END {define.sub_type.get_type().literal} {define.get_descriptor_token().literal}")

    for func in raw_module.function_type_defines:
        compiled_module.append(f"{str_spaces}DEFINE FUNCTION_SIGNATURE {func.get_descriptor_token().literal}")
        compiled_module.append(f"{str_spaces}{str_spaces}RETURN_TYPE {func.get_value_token().literal}")
        for param in func.get_arg_list():
            compiled_module.append(f"{str_spaces}{str_spaces}PARAMETER {param.literal}")
        compiled_module.append(f"{str_spaces}END FUNCTION_SIGNATURE {func.get_descriptor_token().literal}")