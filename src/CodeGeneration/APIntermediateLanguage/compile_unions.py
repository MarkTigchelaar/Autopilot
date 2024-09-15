def compile_unions(raw_module, compiled_module, symbol_table, spaces):
    str_spaces = " " * spaces
    for union in raw_module.unions:
        compiled_module.append(f"{str_spaces}DEFINE UNION {union.get_name().literal}")

        for union_value in union.items:
            compiled_module.append(
                f"{str_spaces}{str_spaces}FIELD {union_value.item_name_token.literal} {union_value.type_token.literal}"
            )
        compiled_module.append(f"{str_spaces}END UNION {union.get_name().literal}")
