import os
from Testing.progress_tracker import ProgressTracker
from Testing.utils import (
    open_json,
    object_to_json,
    check_errors_as_json,
    check_token_data_as_json_w_eof,
)
from ErrorHandling.tokenizer_error_manager import TokenizerErrorManager
from Tokenization.tokenizer import Tokenizer


def run_tokenization_tests(progress_tracker: ProgressTracker) -> None:
    manual_tests = open_json("Testing/Tokenization/manual_tests.json")
    manual_test_case_folder = "Testing/Tokenization/ManualTestCases"
    print("Running manually made tokenizer tests")
    run_tests(manual_tests, manual_test_case_folder, progress_tracker)
    print("Running automatically generated tokenizer tests")
    auto_tests = open_json("Testing/Tokenization/script_generated_tests.json")
    auto_test_case_folder = "Testing/Tokenization/ScriptGeneratedTestCases"
    run_tests(auto_tests, auto_test_case_folder, progress_tracker)


def run_tests(
    manual_tests: list, test_case_folder: str, progress_tracker: ProgressTracker
) -> None:
    for test in manual_tests:

        path = os.path.join(os.getcwd(), test_case_folder)
        file_path = os.path.join(path, test["file_name"])
        error_manager = TokenizerErrorManager()
        tokenizer = Tokenizer(error_manager)

        tokenizer.tokenize_file(file_path)

        check_results(tokenizer, error_manager, test, path, progress_tracker)


def check_results(
    tokenizer: Tokenizer,
    error_manager: TokenizerErrorManager,
    test: dict,
    file_path: str,
    progress_tracker: ProgressTracker,
) -> None:
    expected_tokens = test["tokens"]

    token_list = tokenizer.get_tokens()
    if error_manager.has_errors() and len(token_list) > 0:
        raise Exception("Tokenizer has errors and tokens, illegal state!")

    if error_manager.has_errors():
        actual_errors = object_to_json(error_manager.get_errors())
        expected_errors = [test["error"]]
        check_errors_as_json(
            actual_errors, expected_errors, test, file_path, progress_tracker
        )
    else:
        token_as_json_list = object_to_json(token_list)
        if len(token_as_json_list) != len(expected_tokens) + 1:
            progress_tracker.add_error_message(
                f"Token count mismatch for {test['file_name']}. Expected: {len(expected_tokens)}, but got: {len(token_as_json_list)}"
            )
        else:
            check_token_data_as_json_w_eof(
                token_as_json_list, expected_tokens, test, file_path, progress_tracker
            )
