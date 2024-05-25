
from Tokenization.tokenizer import Tokenizer
from ErrorHandling.error_manager import ErrorManager
from driver import Driver
from Parsing.parse import parse_src
from TestingComponents.testing_utilities import (
    get_json_from_file,
    record_component_test,
    make_analyzer,
)


def phase_four_tests(tracker, test_json, current_dir):
    test_control_function(tracker, test_json, current_dir, "Phase 4 tests")

def test_control_function(tracker, test_json, current_dir, phase_name):
    print(phase_name)
    for test in test_json:
        component_tests = get_json_from_file(
            current_dir + "/" + test["test_manifest_file"]
        )
        general_component = test["general_component"]
        print(f"Targeted component(s): {general_component}")
        run_tests(component_tests, current_dir, tracker)


def run_tests(component_tests, current_dir, tracker):
    for test_case in component_tests:
        skip = False
        # for test in test_case["files"]:
        #     if "Test12" not in test:
        #         skip = True
        #         break
        if not skip:
            semantic_test(test_case, current_dir, tracker)


def semantic_test(test_case, current_dir, tracker):
    err_manager = ErrorManager()
    analyzer = make_analyzer(err_manager, test_case)

    for i in range(len(test_case["files"])):
        tokenizer = Tokenizer(err_manager)
        try:
            tokenizer.load_src(test_case["files"][i])
        except:
            tokenizer.load_src(current_dir + "/" + test_case["files"][i])
        driver = Driver(tokenizer, err_manager, analyzer)
        _ = parse_src(driver)
        tokenizer.close_src()
    if not err_manager.has_errors():
        analyzer.run_global_analysis()

    check_for_token_and_parser_errors(err_manager, test_case, tracker)
    validate_results(err_manager, test_case, tracker)


def validate_results(err_manager, test_case, tracker):
    expected_errors = test_case["errors"]
    if len(expected_errors) == 0 and not err_manager.has_errors():
        test_case["file"] = test_case["files"][0]
        record_component_test(test_case, tracker, "no error", "no error")

    elif len(expected_errors) > 0 and not err_manager.has_errors(True):
        num_errors = len(err_manager.semantic_errors)
        num_expected_errors = len(expected_errors)
        raise Exception(
            f"INTERNAL ERROR: ErrorManager is missing errors for test: {expected_errors[0]['file']}, expected error: {expected_errors}. \nNumber of errors: {num_errors}, number of expected errors: {num_expected_errors}"
        )
    for expected_error in expected_errors:

        actual_error = err_manager.next_semantic_error()
        test_case["file"] = expected_error["file"]
        record_component_test(
            test_case, tracker, expected_error["file"], actual_error.token.file_name
        )
        record_component_test(
            test_case,
            tracker,
            expected_error["token_literal"],
            actual_error.token.literal,
        )
        record_component_test(
            test_case,
            tracker,
            expected_error["line_number"],
            actual_error.token.line_number,
        )
        record_component_test(
            test_case,
            tracker,
            expected_error["column"],
            actual_error.token.column_number,
        )
        record_component_test(
            test_case, tracker, expected_error["message"], actual_error.message
        )
        if actual_error.shadowed_token:
            record_component_test(
                test_case,
                tracker,
                expected_error["shadowed_file"],
                actual_error.shadowed_token.file_name,
            )
            record_component_test(
                test_case,
                tracker,
                expected_error["shadowed_token_literal"],
                actual_error.shadowed_token.literal,
            )
            record_component_test(
                test_case,
                tracker,
                expected_error["shadowed_line_number"],
                actual_error.shadowed_token.line_number,
            )
            record_component_test(
                test_case,
                tracker,
                expected_error["shadowed_column"],
                actual_error.shadowed_token.column_number,
            )
        else:
            record_component_test(
                test_case, tracker, expected_error["shadowed_file"], None
            )
            record_component_test(
                test_case, tracker, expected_error["shadowed_token_literal"], None
            )
            record_component_test(
                test_case, tracker, expected_error["shadowed_line_number"], None
            )
            record_component_test(
                test_case, tracker, expected_error["shadowed_column"], None
            )

    if err_manager.has_errors(True):
        while err_manager.has_errors(True):
            actual_error = err_manager.next_semantic_error()
            print(actual_error.token.file_name)
            print(actual_error.token.literal)
            print(actual_error.token.line_number)
            print(actual_error.token.column_number)
            print(actual_error.message)
            record_component_test(test_case, tracker, "no error", "error")

        print("INTERNAL ERROR: ErrorManager has extra errors")


# Should be treated as private, but exception made for testing code
def check_for_token_and_parser_errors(err_manager, test_case, tracker):
    if len(err_manager.tokenizer_errors) > 0:
        raise Exception(
            "INTERNAL ERROR: tokenizer error(s) found in semantic analysis test"
        )
    elif len(err_manager.parser_errors) > 0:
        while err_manager.has_errors(True):
            actual_error = err_manager.next_parser_error()
            print(actual_error.token.file_name)
            print(actual_error.token.literal)
            print(actual_error.token.line_number)
            print(actual_error.token.column_number)
            print(actual_error.message)
            record_component_test(test_case, tracker, "no error", "error")
