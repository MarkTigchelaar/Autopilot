from .compile_functions import compile_functions

def compile_structs(raw_module, compiled_module, symbol_table, spaces):
    str_spaces = " " * spaces
    for struct in raw_module.structs:
        inline_token = struct.get_inline_token()
        type_modifier = "INLINE_" if inline_token is not None else ""
        compiled_module.append(f"{str_spaces}DEFINE {type_modifier}STRUCT {struct.get_name().literal}")
        for interface in struct.get_interfaces():
            compiled_module.append(f"{str_spaces}{str_spaces}DEFINE INTERFACE {interface.literal}")

        for field in struct.get_fields():
            compiled_module.append(f"{str_spaces}{str_spaces}DEFINE FIELD {field.field_name_token.literal} {field.type_token.literal}")


        compile_functions(struct, compiled_module, symbol_table, spaces + 4)
        compiled_module.append(f"{str_spaces}END {type_modifier}STRUCT {struct.get_name().literal}")
    return compiled_module