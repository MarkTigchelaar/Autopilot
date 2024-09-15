from .compile_header import compile_header

def compile_interfaces(raw_module, compiled_module, symbol_table, spaces):
    str_spaces = " " * spaces
    for interface in raw_module.interfaces:
        compiled_module.append(f"{str_spaces}DEFINE INTERFACE {interface.get_name().literal}")
        for fn_header in interface.fn_headers:
            compiled_module.append(
                f"{str_spaces}{str_spaces}DEFINE FUNCTION_SIGNATURE {fn_header.get_name().literal}"
            )
            compile_header(fn_header, compiled_module, spaces, spaces)
            compiled_module.append(
                f"{str_spaces}{str_spaces}END FUNCTION_SIGNATURE {fn_header.get_name().literal}"
            )
        compiled_module.append(f"{str_spaces}END INTERFACE {interface.get_name().literal}")
