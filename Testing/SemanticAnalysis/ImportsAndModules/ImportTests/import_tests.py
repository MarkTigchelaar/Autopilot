from Testing.progress_tracker import ProgressTracker
from Parsing.parser import Parser
from Testing.utils import open_json, compare_json, object_to_json
from ErrorHandling.semantic_error_manager import SemanticErrorManager
from SemanticAnalysis.ImportsAndModules.module_uniqueness import (
    check_for_module_uniqueness,
)
from SemanticAnalysis.ImportsAndModules.import_analysis import check_imports
import json

def run_import_tests(progress_tracker: ProgressTracker) -> None:
    import_tests = open_json(
        "Testing/SemanticAnalysis/ImportsAndModules/ImportTests/import_tests.json"
    )
    test_case_folder = (
        "Testing/SemanticAnalysis/ImportsAndModules/ImportTests/TestCases/"
    )

    for test in import_tests:
        run_test(test, test_case_folder, progress_tracker)




def run_test(test, test_case_folder, progress_tracker):
    parser = Parser("current_working_dir_not_used_in_these_tests")
    for file in test["files"]:
        file_path = test_case_folder + file["path"]
        module_name = file["module_name"]
        parser.parse_module(file_path, module_name)
    detected_syntax_errors = parser.get_errors()
    assert len(detected_syntax_errors) == 0
    detected_semantic_errors = parser.get_semantic_errors()
    assert len(detected_semantic_errors) == 0

    semantic_error_manager = SemanticErrorManager()
    check_for_module_uniqueness(semantic_error_manager, parser.get_raw_modules())
    check_imports(semantic_error_manager, parser.get_raw_modules())


    detected_errors = semantic_error_manager.get_errors()
    expected_errors = test["errors"]
    num_detected_errors = len(detected_errors)
    num_expected_errors = len(expected_errors)
    #print(f"d errors: {num_detected_errors} e errors: {num_expected_errors}")
    #print(detected_errors)
    assert num_detected_errors == num_expected_errors

    for i, err in enumerate(detected_errors):
        expected_error = expected_errors[i]
        # Path matching is not being tested here

        err_json = object_to_json(err)
        expected_error["token"]["file_path"] = err_json["token"]["file_path"]
        if "shadowed_token" in err_json and err_json["shadowed_token"]:
            expected_error["shadowed_token"]["file_path"] = err_json["shadowed_token"]["file_path"]
        # try:
        #     expected_error["token"]["file_path"] = err_json["token"]["file_path"]
        #     if "shadowed_token" in err_json:
        #         expected_error["shadowed_token"]["file_path"] = err_json["shadowed_token"]["file_path"]
        # except:
        #     print(err_json["token"]["file_path"])
        #     try:
        #         err_json["token"]["file_path"] = None
        #         if "shadowed_token" in err_json:
        #             err_json["shadowed_token"]["file_path"] = None
        #     except:
        #         print("That didnt work either")
        #print(json.dumps(err_json, indent=2))
        #print(json.dumps(expected_error, indent=2))
        compare_json(expected_error, err_json, progress_tracker, file_path)
        # try:
        #     compare_json(expected_error, err_json, progress_tracker, file_path)
        # except:
        #     print("meh!")