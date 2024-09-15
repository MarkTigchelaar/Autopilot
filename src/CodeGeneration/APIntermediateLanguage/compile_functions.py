from .compile_header import compile_header
from .compile_statements import compile_statements

def compile_functions(raw_module, compiled_module, symbol_table, spaces):
    str_spaces = " " * spaces
    for function in raw_module.functions:
        inline_token = function.get_inline_token()
        type_modifier = "INLINE_" if inline_token is not None else ""
        compiled_module.append(f"{str_spaces}DEFINE {type_modifier}FUNCTION {function.get_name_token().literal}")
        compile_header(function.get_header(), compiled_module, spaces)
        compile_statements(function.get_statements(), compiled_module, spaces)
        compiled_module.append(f"{str_spaces}END {type_modifier}FUNCTION {function.get_name_token().literal}")
    return compiled_module
