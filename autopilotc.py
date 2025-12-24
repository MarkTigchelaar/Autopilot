from argparse import ArgumentParser
import os
import json
from typing import List


from Parsing.parser import Parser
from ASTComponents.AggregatedComponents.modules import RawModuleCollection, RawModule
from ErrorHandling.semantic_error_manager import SemanticErrorManager
from ErrorHandling.module_dependency_error_manager import (
    ModuleDependencyCycleErrorManager,
)

from ErrorHandling.parser_error import ParserError
from ErrorHandling.semantic_error import SemanticError
from ErrorHandling.module_dependency_error import ModuleDependencyError

from SemanticAnalysis.ImportsAndModules.module_uniqueness import (
    check_for_module_uniqueness,
)
from SemanticAnalysis.ImportsAndModules.module_dependency_checks import (
    ModuleDependencyChecker,
)
from SemanticAnalysis.LocalAnalysis.local_semantic_analysis import LocalSemanticAnalyzer
from SemanticAnalysis.type_assignment import TypeResolver
# from CodeGeneration.make_code_generator import make_code_generator
# from CodeGeneration.code_generator import CodeGenerator

# Temporary, until ErrorReporter class(es) are created
from Testing.utils import object_to_json


def main():
    args = parse_args()
    print(f"args: {args}")
    current_dir = set_compiler_working_directory(args["current_directory"])
    project_directory = args["project_directory"] if args["project_directory"] else ""
    parser = Parser(current_dir)
    parser.parse_source(project_directory)

    # Autopilot halts compilation at several stages:

    # If any module(s) have syntax errors
    if found_and_reported_syntax_errors(parser):
        return

    # Missing modules, or multiple versions of modules found while resolving one or
    # more import statements
    if found_and_reported_module_existance_errors(parser):
        return

    # Collection of ASTs for all types in all modules of the entire program
    raw_module_collection: RawModuleCollection = parser.get_raw_modules()

    # Duplicate modules of same name, imported by seperate modules, not counting as
    # previous mentioned error type where two modules found on ambigous import paths
    if found_and_reported_module_name_uniqueness_errors(raw_module_collection):
        return

    if found_and_reported_circular_imports(raw_module_collection):
        return
    
    if found_and_reported_local_semantic_errors(raw_module_collection):
        return
    
    if found_and_reported_module_level_errors(raw_module_collection):
        return
    
    if found_and_reported_import_item_existance_errors(raw_module_collection):
        return

    if found_and_reported_type_resolution_errors(raw_module_collection):
        return


    # code_generator: CodeGenerator = make_code_generator("go", raw_module_collection)
    # code_generator.generate_code()
    # code_generator.trigger_output()


def set_compiler_working_directory(working_directory_name: str) -> str:
    os.chdir(working_directory_name)
    return os.getcwd()


"""
    The autopilot compiler is meant to be called by a compiled script, 
    or a bash script on the system path.
    This code could be changed to be packaged, in order to be callable directly, but that would be a large refactor.
"""


def parse_args():
    return {
        "current_directory" : "D:\Projects\Python-Projects\Autopilot\Testing\Temp",
        "project_directory" : None
    }
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "--current_directory",
        dest="current_directory",
        type=str,
        help="Location in filesystem where the compiler is being called from, is sent in by script which calls compiler, not the user.",
        required=True,
    )

    arg_parser.add_argument(
        "--project_directory",
        dest="project_directory",
        type=str,
        help="Location in filesystem of the main module of a project, is expected to usually be current_directory, but could be a different location. argument from user",
        required=True,
    )

    args = arg_parser.parse_args()

    return vars(args)


def found_and_reported_syntax_errors(parser: Parser) -> bool:
    halt_compiler = False
    syntax_errors = parser.get_errors()
    if syntax_errors and len(syntax_errors) > 0:
        report_syntax_errors(syntax_errors)
        halt_compiler = True
    return halt_compiler


def report_syntax_errors(syntax_errors: List[ParserError]):
    for error in syntax_errors:
        err_json = object_to_json(error)
        print(json.dumps(err_json, indent=4))


def found_and_reported_module_existance_errors(parser: Parser) -> bool:
    halt_compiler = False
    semantic_errors = parser.get_semantic_errors()
    if semantic_errors and len(semantic_errors) > 0:
        report_semantic_errors(semantic_errors)
        halt_compiler = True

    return halt_compiler


def report_semantic_errors(semantic_errors: List[SemanticError]):
    for error in semantic_errors:
        err_json = object_to_json(error)
        print(json.dumps(err_json, indent=4))


def found_and_reported_module_name_uniqueness_errors(
    raw_module_collection: RawModuleCollection,
) -> bool:
    generic_semantic_error_manager = SemanticErrorManager()
    check_for_module_uniqueness(generic_semantic_error_manager, raw_module_collection)
    halt_compiler = generic_semantic_error_manager.has_errors()
    if halt_compiler:
        report_semantic_errors(generic_semantic_error_manager.get_errors())
    return halt_compiler


def found_and_reported_circular_imports(
    raw_module_collection: RawModuleCollection,
) -> bool:
    module_dependency_checker = make_module_dependency_checker(raw_module_collection)
    module_dependency_checker.build_dependency_graph()
    module_dependency_checker.check_dependency_graph()
    circular_import_error_manager = module_dependency_checker.get_error_manager()
    halt_compiler = circular_import_error_manager.has_errors()
    if halt_compiler:
        report_module_dependency_cycle_errors(
            circular_import_error_manager.get_errors()
        )
    return halt_compiler

def make_module_dependency_checker(raw_module_collection: RawModuleCollection) -> ModuleDependencyChecker:
    circular_import_error_manager = ModuleDependencyCycleErrorManager()
    return ModuleDependencyChecker(
        circular_import_error_manager, raw_module_collection
    )

def report_module_dependency_cycle_errors(errors: List[ModuleDependencyError]):
    for error in errors:
        error_json = object_to_json(error)
        print(json.dumps(error_json, indent=4))


def found_and_reported_local_semantic_errors(raw_module_collection: RawModuleCollection) -> bool:
    error_manager = SemanticErrorManager()
    local_analyzer = LocalSemanticAnalyzer(raw_module_collection, error_manager)
    local_analyzer.analyze_program()
    halt_compiler = error_manager.has_errors()
    if halt_compiler:
        report_semantic_errors(error_manager.get_errors())
    return halt_compiler


def found_and_reported_module_level_errors(raw_module_collection: RawModuleCollection):
    raw_module_collection.check_modules()
    halt_compiler = raw_module_collection.has_errors()
    if halt_compiler:
        error_manager = raw_module_collection.get_error_manager()
        report_semantic_errors(error_manager)
    return halt_compiler


def found_and_reported_import_item_existance_errors(raw_module_collection: RawModuleCollection):
    raw_module_collection.check_imports_for_existing_items()
    halt_compiler = raw_module_collection.has_errors()
    if halt_compiler:
        error_manager = raw_module_collection.get_error_manager()
        report_semantic_errors(error_manager)
    return halt_compiler

def found_and_reported_type_resolution_errors(raw_module_collection: RawModuleCollection):
    type_resolver = TypeResolver(raw_module_collection)
    type_resolver.resolve_types()
    halt_compiler = raw_module_collection.has_errors()
    if halt_compiler:
        error_manager = raw_module_collection.get_error_manager()
        report_semantic_errors(error_manager)
    return halt_compiler

if __name__ == "__main__":
    main()
