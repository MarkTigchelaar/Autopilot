from Testing.progress_tracker import ProgressTracker
from Parsing.parser import Parser
from Testing.utils import open_json, compare_json, object_to_json
from ErrorHandling.module_dependency_error_manager import ModuleDependencyCycleErrorManager
from SemanticAnalysis.ImportsAndModules.module_dependency_checks import (
    ModuleDependencyChecker
)
import os

"""
For testing:
    Parsers ability to find modules
    Parsers ability to form dependency graphs for modules
    ModuleDependencyCheckers ability to detect cycles in the dependency graph of modules
"""

def run_module_dependency_tests(progress_tracker: ProgressTracker) -> None:
    module_dependency_tests = open_json(
        "Testing/SemanticAnalysis/ImportsAndModules/ModuleDependencyGraphs/module_dependency_tests.json"
    )
    test_case_folder = "TestCases"
    

    abs_location_of_this_python_file = os.path.dirname(__file__)
    path_to_test_cases = os.path.normpath(abs_location_of_this_python_file + "/" + test_case_folder)

    for test in module_dependency_tests:
        run_test(test, path_to_test_cases, progress_tracker)




def run_test(test, test_case_folder, progress_tracker):
    parser = Parser(test_case_folder)
    parser.parse_source("/" + test["main_module_path"])

    detected_syntax_errors = parser.get_errors()

    assert len(detected_syntax_errors) == 0
    detected_semantic_errors = parser.get_semantic_errors()

    assert len(detected_semantic_errors) == 0

    semantic_error_manager = ModuleDependencyCycleErrorManager()
    module_dependency_graph_checker = ModuleDependencyChecker(semantic_error_manager, parser.get_raw_modules())

    module_dependency_graph_checker.build_dependency_graph()
    module_dependency_graph_checker.check_dependency_graph()

    detected_errors = semantic_error_manager.get_errors()
    expected_errors = test["errors"]
    num_detected_errors = len(detected_errors)
    num_expected_errors = len(expected_errors)
    assert num_detected_errors == num_expected_errors

    for i, err in enumerate(detected_errors):
        expected_error = expected_errors[i]
        err_json = object_to_json(err)
        for i, tok in enumerate(err_json["import_statement_token_dependency_chain"]):
            # This is for avoiding locking in to one location on the filesystem for tests.
            expected_error["import_statement_token_dependency_chain"][i]["file_path"] = tok["file_path"]

        compare_json(expected_error, err_json, progress_tracker, test["main_module_path"])