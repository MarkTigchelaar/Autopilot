""" Autopilot bytecode compiler for the Autopilot programming language

    Version 1.0.0
    Written by Mark Tigchelaar
    2024
"""

import os
import time
from argparse import ArgumentParser
from Parsing.parser import Parser
from CodeGeneration.generate_code import generate_code
from ASTComponents.SystemComponents.built_in_components import get_built_in_library_catalog
#from APIntermediateLanguage.process_ap_ast_to_ir import compile_to_autopilot_intermediate_language
#from APIntermediateLanguage.APILCompiler.main import compile_apil_to_april

def main():
    start_time = time.time()
    # args = collect_args()
    # print(args.input_dir)
    # print(args.output_file)
    input_dir = "/src"
    input_dir = "."
    output_file = "output"

    # parser = configure_parser(args.input_dir)
    # parser.parse_source(args.input_dir)
    parser = configure_parser(input_dir)
    if input_dir == ".":
        input_dir = ""
    parser.parse_source(input_dir)

    if parser.has_errors():
        print("HAS ERRORS!")
        parser.report_errors()
        return
    raw_module_collection = parser.get_raw_modules()
    built_in_library_catalog = get_built_in_library_catalog("python")
    raw_module_collection.add_built_in_libs(built_in_library_catalog)
    # global_scope_type_check(raw_module_collection)
    # if raw_module_collection.has_errors():
    #     raw_module_collection.report_errors()
    #     return

    # dependency_analysis(raw_module_collection)
    # if raw_module_collection.has_errors():
    #     raw_module_collection.report_errors()
    #     return

    generate_code(raw_module_collection, output_file, "python")
    elapsed_time = time.time() - start_time
    print(f"Compilation took {elapsed_time} seconds")


    




def configure_parser(input_dir):

    current_dir = os.getcwd()
    if input_dir == ".":
        input_dir = current_dir
    else:
        input_dir = current_dir + "\\" + input_dir
    normalized_path = os.path.normpath(input_dir)
    if not os.path.exists(normalized_path):
        print(f"Input directory does not exist: {normalized_path}")
        print("run compiler within same directory structure as input directory")
        print(f"Current directory: {current_dir}")
        print("Exiting...")
        return
    parser = Parser(current_dir)
    return parser

def collect_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", help="Input directory of main module to autopilot")
    parser.add_argument("output_file", help="Output file name and path for autopilot write to")
    return parser.parse_args()

if __name__ == "__main__":
    main()
