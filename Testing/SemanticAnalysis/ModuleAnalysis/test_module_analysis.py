import os
from Testing.progress_tracker import ProgressTracker
from Parsing.parser import Parser
from Testing.utils import open_json, object_to_json, compare_json


def run_module_analysis_tests(progress_tracker: ProgressTracker) -> None:
    module_dependency_tests = open_json(
        "Testing/SemanticAnalysis/ModuleAnalysis/tests.json"
    )
    test_case_folder = "TestCases"
    abs_location_of_this_python_file = os.path.dirname(__file__)
    path_to_test_cases = os.path.normpath(
        abs_location_of_this_python_file + "/" + test_case_folder
    )

    for test in module_dependency_tests:
        run_test(test, path_to_test_cases, progress_tracker)


def run_test(test, test_case_folder, progress_tracker):
    parser = Parser(test_case_folder)
    parser.parse_source("/" + test["main_module_path"])

    detected_syntax_errors = parser.get_errors()
    for err in detected_syntax_errors:
        as_json = object_to_json(err)
        print(as_json)

    assert len(detected_syntax_errors) == 0
    detected_semantic_errors = parser.get_semantic_errors()

    for err in detected_semantic_errors:
        as_json = object_to_json(err)
        print(as_json)
    assert len(detected_semantic_errors) == 0

    parsed_modules = parser.get_raw_modules()
    parsed_modules.check_modules()
    error_manager = parsed_modules.get_error_manager()
    detected_errors = error_manager.get_errors()
    if test["errors"] is None:
        test["errors"] = []
    assert len(detected_errors) == len(test["errors"])

    for i, err in enumerate(detected_errors):
        expected_error = test["errors"][i]
        err_json = object_to_json(err)
        err_json["token"]["file_path"] = None
        if "shadowed_token" in err_json and err_json["shadowed_token"]:
            err_json["shadowed_token"]["file_path"] = None
        if "lhs_type_token" in err_json and err_json["lhs_type_token"]:
            err_json["lhs_type_token"]["file_path"] = None
        if "rhs_type_token" in err_json and err_json["rhs_type_token"]:
            err_json["rhs_type_token"]["file_path"] = None

        compare_json(
            expected_error, err_json, progress_tracker, test["main_module_path"]
        )
