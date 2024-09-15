def compile_header(fn_header, compiled_module, spaces, extra_space=0):
    str_spaces = " " * spaces
    str_extra_spaces = " " * extra_space if extra_space > 0 else ""
    return_type = "null"
    if fn_header.get_return_type() is not None:
        return_type = fn_header.get_return_type().literal
    compiled_module.append(
        f"{str_spaces}{str_spaces}{str_extra_spaces}RETURN_TYPE {return_type}"
    )
    for arg in fn_header.get_args():
        default_value = ""
        default_value_token = arg.get_default_value()
        if default_value_token is not None:
            default_value = f"{default_value_token.literal}"

        compiled_module.append(
            f"{str_spaces}{str_spaces}{str_extra_spaces}ARGUMENT {arg.get_type().literal} {arg.get_name().literal} {default_value}"
        )
