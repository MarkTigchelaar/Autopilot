from Testing.progress_tracker import ProgressTracker
from Parsing.parser import Parser
from Testing.utils import open_json, compare_json, object_to_json
from ErrorHandling.semantic_error_manager import SemanticErrorManager
from SemanticAnalysis.ImportsAndModules.module_uniqueness import (
    check_for_module_uniqueness,
)
import json

def run_module_uniqueness_tests(progress_tracker: ProgressTracker) -> None:
    uniqueness_tests = open_json(
        "Testing/SemanticAnalysis/ImportsAndModules/ModuleUniqueness/module_uniqueness_tests.json"
    )
    test_case_folder = (
        "Testing/SemanticAnalysis/ImportsAndModules/ModuleUniqueness/TestCases/"
    )

    for test in uniqueness_tests:
        run_test(test, test_case_folder, progress_tracker)



def run_test(test, test_case_folder, progress_tracker):
    parser = Parser("current_working_dir_not_used_in_these_tests")
    for file in test["files"]:
        file_path = test_case_folder + file["path"]
        module_name = file["module_name"]
        parser.parse_module(file_path, module_name)

    detected_syntax_errors = parser.get_errors()
    assert len(detected_syntax_errors) == 0
    semantic_error_manager = SemanticErrorManager()
    check_for_module_uniqueness(semantic_error_manager, parser.get_raw_modules())

    detected_errors = semantic_error_manager.get_errors()
    expected_errors = test["errors"]
    for i, err in enumerate(detected_errors):
        expected_error = expected_errors[i]
        # Path matching is not being tested here

        err_json = object_to_json(err)
        try:
            expected_error["token"]["file_path"] = err_json["token"]["file_path"]
            expected_error["shadowed_token"]["file_path"] = err_json["shadowed_token"]["file_path"]
        except:
            print(err_json["token"]["file_path"])
            err_json["token"]["file_path"] = None
            err_json["shadowed_token"]["file_path"] = None
            print(json.dumps(err_json, indent=2))
        try:
            compare_json(expected_error, err_json, progress_tracker, file_path)
        except:
            print("meh!")