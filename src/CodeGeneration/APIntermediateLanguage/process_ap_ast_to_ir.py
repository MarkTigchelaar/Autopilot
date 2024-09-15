"""Autopilot intermediate language compiler for the Autopilot programming language
    Takes AST of Autopilot program, and converts this to a 3 address code like flat intermediate language
    This language has no scope, and simple syntax
    Global semantic analysis is already done before using this langauge in the next phase of the compiler.
    This is simply to reduce autopilot code down to bytecode in steps.

    Version 1.0
    Written by Mark Tigchelaar
    2024

"""

from symbols import *
from .compile_imports import compile_imports
from .compile_enums import compile_enums
from .compile_errors import compile_errors
from .compile_defines import compile_defines
from .compile_unions import compile_unions
from .compile_interfaces import compile_interfaces
from .compile_functions import compile_functions
from .compile_unittests import compile_unittests
from .compile_structs import compile_structs


# Module level analysis can be done on the raw modules ast to check for errors
# but global scope is too big, and would be very cumbersome
# A fast lookup table is needed to check for symbol types
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, symbol, symbol_type):
        self.symbols[symbol] = symbol_type

    def get_symbol_type(self, symbol):
        return self.symbols[symbol]


class APILProgram:
    def __init__(self, compiled_modules, symbol_table, error_manager):
        self.compiled_modules = compiled_modules
        self.symbol_table = symbol_table
        self.error_manager = error_manager

    def has_errors(self):
        return self.error_manager.has_errors()

    def report_errors(self):
        self.error_manager.report_errors()

    def write_to_file(self, file_name):
        with open(file_name, "w") as file:
            for line in self.compiled_modules:
                file.write(line + "\n")


def compile_to_ap_bytecode(raw_module_collection, output_file):
    pass
    #compiled_modules = compile_to_autopilot_intermediate_language(raw_module_collection)
    # compiled_modules.write_to_file(output_file)
    # april_program = compile_apil_to_april(apil_program.compiled_modules)
    # assembly_program = compile_to_assembly(optimized_program)
    # generate_bytecode(assembly_program, output_file.apbc)

def compile_to_autopilot_intermediate_language(raw_module_collection):
    compiled_modules = []
    symbol_table = SymbolTable()
    for raw_module in raw_module_collection.get_raw_modules():
        compiled_module = compile_module(raw_module, symbol_table)
        compiled_modules.extend(compiled_module)

    return APILProgram(
        compiled_modules, symbol_table, raw_module_collection.get_error_manager()
    )


def compile_module(raw_module, symbol_table):
    compiled_module = []
    spaces = 4
    compiled_module.append(f"DEFINE MODULE {raw_module.name}")
    compile_imports(raw_module, compiled_module, symbol_table, spaces)
    compile_defines(raw_module, compiled_module, symbol_table, spaces)
    compile_enums(raw_module, compiled_module, symbol_table, spaces)
    compile_errors(raw_module, compiled_module, symbol_table, spaces)
    compile_unions(raw_module, compiled_module, symbol_table, spaces)
    compile_interfaces(raw_module, compiled_module, symbol_table, spaces)
    compile_structs(raw_module, compiled_module, symbol_table, spaces)
    compile_functions(raw_module, compiled_module, symbol_table, spaces)
    compile_unittests(raw_module, compiled_module, symbol_table, spaces)
    compiled_module.append(f"END MODULE {raw_module.name}")
    return compiled_module
