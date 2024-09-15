from .compile_statements import compile_statements


def compile_unittests(raw_module, compiled_module, symbol_table, spaces):
    str_spaces = " " * spaces
    for unit_test in raw_module.unit_tests:
        compiled_module.append(
            f"{str_spaces}DEFINE UNITTEST {unit_test.get_name_token().literal}"
        )
        compile_statements(unit_test.get_statements(), compiled_module, spaces)
        compiled_module.append(
            f"{str_spaces}END UNITTEST {unit_test.get_name_token().literal}"
        )
    return compiled_module
