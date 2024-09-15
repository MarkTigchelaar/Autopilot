def compile_errors(raw_module, compiled_module, symbol_table, spaces):
    str_spaces = " " * spaces
    for error in raw_module.errors:
        compiled_module.append(f"{str_spaces}DEFINE ERROR {error.get_name().literal}")
        for error_field in error.items:
            compiled_module.append(f"{str_spaces}{str_spaces}FIELD {error_field.literal}")
        compiled_module.append(f"{str_spaces}END ERROR {error.get_name().literal}")
    return compiled_module
