from typing import List, Dict, Any, Tuple
from Testing.progress_tracker import ProgressTracker
import os
from typing import Optional, Any, Dict
from ErrorHandling.tokenizer_error_manager import TokenizerErrorManager
from ErrorHandling.parser_error_manager import ParsingErrorManager
from Tokenization.tokenizer import Tokenizer
from Parsing.driver import Driver

EXPECTED_OUTPUT_FOLDER_NAME = "AstFiles"


def open_json(file_path: str) -> dict:
    """
    Open a JSON file and return its contents as a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file.
    """
    import json

    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def object_to_json(object_instance):
    if object_instance is None:
        return None
    if isinstance(object_instance, list):
        return [object_to_json(i) for i in object_instance]
    j = object_instance
    if not isinstance(object_instance, dict):
        j = object_instance.__dict__
    j["type_def"] = str(type(object_instance).__name__)
    for key in j:
        if str(type(j[key]).__name__) not in ("int", "str", "float", "bool"):
            j[key] = object_to_json(j[key])
    return j


def check_token_data_as_json_w_eof(
    token_as_json_list: list,
    expected_tokens: list,
    test: dict,
    file_path: str,
    progress_tracker: ProgressTracker,
) -> None:
    check_token_data_as_json(
        token_as_json_list[:-1],
        expected_tokens,
        test,
        file_path,
        progress_tracker,
    )
    check_result(
        token_as_json_list[-1]["internal_type"],
        "Token internal type",
        "EOF",
        progress_tracker,
        test["file_name"],
    )


def check_token_data_as_json(
    token_as_json_list: list,
    expected_tokens: list,
    test: dict,
    file_path: str,
    progress_tracker: ProgressTracker,
) -> None:
    for i in range(len(token_as_json_list)):
        check_result(
            token_as_json_list[i]["literal"],
            "Token literal",
            expected_tokens[i]["literal"],
            progress_tracker,
            test["file_name"],
        )
        check_result(
            token_as_json_list[i]["file_name"],
            "File name",
            expected_tokens[i]["file_name"],
            progress_tracker,
            test["file_name"],
        )
        check_result(
            token_as_json_list[i]["file_path"],
            "File path",
            file_path + "/",
            progress_tracker,
            test["file_name"],
        )
        check_result(
            token_as_json_list[i]["line_number"],
            "Line number",
            expected_tokens[i]["line_number"],
            progress_tracker,
            test["file_name"],
        )
        check_result(
            token_as_json_list[i]["column_number"],
            "Column number",
            expected_tokens[i]["column_number"],
            progress_tracker,
            test["file_name"],
        )


def check_errors_as_json(
    errors: List[Dict[str, Any]],
    expected_errors: List[Dict[str, Any]],
    test: dict,
    file_path: str,
    progress_tracker: ProgressTracker,
) -> None:
    if len(errors) != len(expected_errors):
        progress_tracker.add_error_message(
            f"Error count mismatch for {test['file_name']}. Expected: {len(expected_errors)}, but got: {len(errors)}"
        )
        return
    for i in range(len(errors)):
        check_result(
            errors[i]["message"],
            "Error message",
            expected_errors[i]["message"],
            progress_tracker,
            test["file_name"],
        )
        check_result(
            errors[i]["type_def"],
            "Error Type Definition",
            expected_errors[i]["type_def"],
            progress_tracker,
            test["file_name"],
        )
        check_token_data_as_json(
            [errors[i]["token"]],
            [expected_errors[i]["token"]],
            test,
            file_path,
            progress_tracker,
        )
        if "shadowed_token" in expected_errors[i] and expected_errors[i]["shadowed_token"]:
            check_token_data_as_json(
                [errors[i]["shadowed_token"]],
                [expected_errors[i]["shadowed_token"]],
                test,
                file_path,
                progress_tracker,
            )


def compare_json(
    expected: Dict[str, Any],
    actual: Dict[str, Any],
    progress_tracker: ProgressTracker,
    test_file_name: str,
) -> None:
    for key in expected:
        if key not in actual:
            raise Exception(f"Key {key} not found in actual {actual} for test {test_file_name}")
        if str(type(expected[key])) != str(type(actual[key])):
            raise Exception(
                f"Expected type of key {key} is {str(type(expected[key]))}, got {str(type(actual[key]))}"
            )
        if isinstance(expected[key], dict):
            compare_json(expected[key], actual[key], progress_tracker, test_file_name)
        elif isinstance(expected[key], list):
            compare_json_lists(
                expected[key], actual[key], progress_tracker, test_file_name
            )
        else:
            check_result(
                actual[key], key, expected[key], progress_tracker, test_file_name
            )


def compare_json_lists(
    expected: List[Any],
    actual: List[Any],
    progress_tracker: ProgressTracker,
    test_file_name: str,
):
    if len(expected) != len(actual):
        raise Exception(
            f"Expected: has length {len(expected)}, actual has length {len(actual)} in test {test_file_name}: {actual}"
        )
    for i in range(len(expected)):
        if isinstance(expected[i], dict):
            compare_json(expected[i], actual[i], progress_tracker, test_file_name)
        elif isinstance(expected[i], list):
            compare_json_lists(expected[i], actual[i], progress_tracker, test_file_name)
        else:
            check_result(
                actual[i],
                "item at index",
                expected[i],
                progress_tracker,
                test_file_name,
            )


def check_result(
    result: str,
    result_attr: str,
    expected_result: str,
    progress_tracker: ProgressTracker,
    test_file_name: str,
) -> None:
    if result != expected_result:
        progress_tracker.add_error_message(
            f"{result_attr} mismatch for {test_file_name}. Expected: {expected_result}, but got: {result}"
        )
    else:
        progress_tracker.inc_success()


def populate_file_path(expected_ast: Dict[str, Any], sample_file_path: str) -> None:
    for key in expected_ast:
        if key == "file_path":
            expected_ast[key] = sample_file_path
        elif isinstance(expected_ast[key], dict):
            populate_file_path(expected_ast[key], sample_file_path)
        elif isinstance(expected_ast[key], list):
            for item in expected_ast[key]:
                if isinstance(item, dict):
                    populate_file_path(item, sample_file_path)


def run_tests(
    test_cases: list,
    test_case_folder: str,
    sample_folder: str,
    expected_output_folder: str,
    progress_tracker: ProgressTracker,
    parse_function,  # function
    unit_testing: bool = True,
) -> None:
    for test in test_cases:
        # if test["file_name"] != "test37.txt":
        #     continue

        path = os.path.join(os.getcwd(), test_case_folder)
        sample_file_path = os.path.join(path, sample_folder)
        if test["ast_file"]:
            expected_ast_tree_path = os.path.join(
                path, expected_output_folder, test["ast_file"]
            )
            assert (
                test["errors"] is None or len(test["errors"]) == 0
            ), f"errors should be empty for {test['file_name']}"
            run_test_w_ast(
                progress_tracker,
                sample_file_path,
                expected_ast_tree_path,
                test,
                parse_function,
                unit_testing,
            )
        else:
            expected_ast_tree_path = None
            assert (
                len(test["errors"]) > 0
            ), f"errors should not be empty for {test['file_name']}"
            run_test_w_errors(
                progress_tracker, sample_file_path, test, parse_function, unit_testing
            )


def local_semantic_analysis_setup(
    sample_file_path: str,
    test: Dict[str, Any],
    parse_function,
    is_unit_testing = True,
):
    ast, parse_error_manager, file_full_path = parsing_setup_function(
        sample_file_path,
        test,
        parse_function,
        is_unit_testing
    )
    if parse_error_manager.has_errors():
        raise Exception(f"Parser error manager has errors in semantic test!\n{object_to_json(parse_error_manager.get_errors())}")
    return ast, file_full_path


def parsing_setup_function(
    sample_file_path: str,
    test: Dict[str, Any],
    parse_function,
    unit_testing: bool,
) -> Tuple[Optional[Any], ParsingErrorManager, str]:
    file_full_path = os.path.join(sample_file_path, test["file_name"])
    parse_error_manager = ParsingErrorManager()
    tokenizer_error_manager = TokenizerErrorManager()
    tokenizer = Tokenizer(tokenizer_error_manager)
    tokenizer.tokenize_file(file_full_path)

    if tokenizer_error_manager.has_errors():
        raise Exception(
            f"Tokenizer error in file {sample_file_path}: {tokenizer_error_manager.get_errors()}"
        )
    driver = Driver(tokenizer, parse_error_manager, testing=unit_testing)

    ast: Optional[Any] = parse_function(driver)
    return ast, parse_error_manager, file_full_path

def run_test_w_ast(
    progress_tracker: ProgressTracker,
    sample_file_path: str,
    expected_ast_tree_path: str,
    test: Dict[str, Any],
    parse_function,
    unit_testing: bool,
) -> None:
    ast, parse_error_manager, file_full_path = parsing_setup_function(
        sample_file_path,
        test,
        parse_function,
        unit_testing
    )

    if ast is None:
        errors_string = ""
        for error in parse_error_manager.get_errors():
            errors_string += error.to_string() + '\n'
        raise Exception(f"AST is None in test {file_full_path}, something is broken: \n{errors_string}")
        

    expected_ast = open_json(expected_ast_tree_path)
    if isinstance(expected_ast, list):
        for item in expected_ast:
            populate_file_path(item, sample_file_path + "/")
    else:
        populate_file_path(expected_ast, sample_file_path + "/")
    ast_as_json = object_to_json(ast)
    # with open("test29_ast.json", "w") as f_it:
    #     json.dump(ast_as_json, f_it, indent=4)
  
    #print(f"AST:\n{json.dumps(ast_as_json)}")
    if isinstance(ast_as_json, list):
        for i in range(len(ast_as_json)):
            compare_json(expected_ast[i], ast_as_json[i], progress_tracker, test["file_name"])
    else:
        compare_json(expected_ast, ast_as_json, progress_tracker, test["file_name"])


def run_test_w_errors(
    progress_tracker: ProgressTracker,
    sample_file_path: str,
    test: Dict[str, Any],
    parse_function,
    unit_testing: bool,
) -> None:

    ast, parse_error_manager, file_full_path = parsing_setup_function(
        sample_file_path,
        test,
        parse_function,
        unit_testing
    )
    if ast:
        raise Exception(f"AST should be None, but got: {ast} in file {file_full_path}")

    if not parse_error_manager.has_errors():
        raise Exception(
            f"Expected a parsing error in file {sample_file_path}, but none occurred."
        )
    actual_errors = object_to_json(parse_error_manager.get_errors())
    check_errors_as_json(
        actual_errors, test["errors"], test, sample_file_path, progress_tracker
    )
