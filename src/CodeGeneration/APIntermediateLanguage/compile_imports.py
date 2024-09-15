def compile_imports(raw_module, compiled_module, symbol_table, spaces):
    str_spaces = " " * spaces

    for import_stmt in raw_module.imports:
        # paths go away because everything is collected into one spot at this point
        compiled_module.append(
            f"{str_spaces}IMPORT {import_stmt.import_type.upper()} {import_stmt.path_list[-1].node_token.literal}"
        )
        for import_item in import_stmt.import_list:
            new_name = (
                import_item.new_name_token.literal
                if import_item.new_name_token
                else import_item.name_token.literal
            )
            compiled_module.append(
                f"{str_spaces}{str_spaces}{str_spaces}ITEM {import_item.name_token.literal} {new_name}"
            )
        compiled_module.append(
            f"{str_spaces}END IMPORT {import_stmt.path_list[-1].node_token.literal}"
        )
    return compiled_module
