import os
from TestingComponents.testing_utilities import get_json_from_file
from Parsing.parser import Parser


def test_full_parser(tracker, current_dir):
    """
    This function will run the tests for phase six of the compiler.
    """
    print("Running phase six tests")
    for test_file_data in TEST_FILES:
        test_name = test_file_data["general_component"]
        test_file = test_file_data["test_manifest_file"]

        print("Running test: " + test_name)
        abs_path = os.path.normpath(current_dir + "\\" + test_file)
        print("Test file abs path: " + abs_path)
        test_json = get_json_from_file(abs_path)
        run_test(tracker, test_json, current_dir + "\\")


def w_newline(string):
    return string + "\n"


def run_test(tracker, test_json, current_dir):
    for test_case in test_json:
        parser = Parser(current_dir)
        parser.parse_source(test_case["entry_dir"])

        if parser.has_errors() and len(test_case["errors"]) == 0:
            tracker.add_error_message(w_newline("Errors found"))
            while parser.has_errors():
                actual_error = parser.error_manager.next_semantic_error()
                tracker.add_error_message(w_newline(actual_error.token.file_name))
                tracker.add_error_message(w_newline(str(actual_error.token.literal)))
                tracker.add_error_message(
                    w_newline(str(actual_error.token.line_number))
                )
                tracker.add_error_message(
                    w_newline(str(actual_error.token.column_number))
                )
                tracker.add_error_message(w_newline(actual_error.message))
            continue
        elif not parser.has_errors() and len(test_case["errors"]) > 0:
            tracker.add_error_message(w_newline("Expected errors, but none found"))
            continue
        elif parser.has_errors() and len(test_case["errors"]) > 0:
            process_errors(tracker, parser, test_case["errors"], current_dir)

        expected_module_count = len(test_case["module_data"])
        actual_module_count = len(parser.raw_modules)
        if expected_module_count != actual_module_count:
            tracker.add_error_message(
                f"Expected {expected_module_count} modules, but found {actual_module_count}"
            )

        else:
            for i in range(expected_module_count):
                check_module_data(
                    tracker,
                    current_dir,
                    test_case["module_data"][i],
                    parser.raw_modules[i],
                )


# use add_error_message to add error messages, do not use inc fail
def check_module_data(tracker, current_dir, expected_module, actual_module):
    if expected_module["name"] != actual_module.name:
        tracker.add_error_message(
            f"Expected module name: {expected_module['name']}, but found {actual_module.name}"
        )
    else:
        tracker.inc_success()

    if expected_module["id"] != actual_module.id:
        tracker.add_error_message(
            f"Expected module id: {expected_module['id']}, but found {actual_module.id}"
        )
    else:
        tracker.inc_success()

    # Normalize the paths to bypass filesystem location differences.
    for i in range(len(expected_module["included_files"])):
        expected_module["included_files"][i] = os.path.normpath(
            current_dir + expected_module["included_files"][i]
        )

    for i in range(len(expected_module["excluded_files"])):
        expected_module["excluded_files"][i] = os.path.normpath(
            current_dir + expected_module["excluded_files"][i]
        )

    if set(expected_module["included_files"]) != set(actual_module.included_files):
        tracker.add_error_message(
            f"Expected module included files: {expected_module['included_files']}, but found {actual_module.included_files}"
        )
    else:
        tracker.inc_success()
    if set(expected_module["excluded_files"]) != set(actual_module.excluded_files):
        tracker.add_error_message(
            f"Expected module excluded files: {expected_module['excluded_files']}, but found {actual_module.excluded_files}"
        )
    else:
        tracker.inc_success()

    import_name_list = [
        import_stmt.path_list[-1].node_token.literal
        for import_stmt in actual_module.imports
    ]
    if set(expected_module["imported_modules"]) != set(import_name_list):
        tracker.add_error_message(
            f"Expected module imports: {expected_module['imports']}, but found {import_name_list}"
        )
    else:
        tracker.inc_success()

    # no more checks are needed, since the components are tested in the previous phases


def process_errors(tracker, parser, test_case_errors, current_dir):
    actual_errors = parser.get_errors()
    if len(test_case_errors) != len(actual_errors):
        tracker.add_error_message(
            f"Expected {len(test_case_errors)} errors, but found {len(actual_errors)}: {test_case_errors} vs {actual_errors}"
        )
    else:
        for i in range(len(test_case_errors)):
            ok = True
            if (
                os.path.normpath(current_dir + "/" + test_case_errors[i]["file"])
                != actual_errors[i].token.file_name
            ):
                ok = False
                tracker.add_error_message(
                    f"Expected error file name: {test_case_errors[i]['file']}, but found {actual_errors[i].token.file_name}"
                )
            if test_case_errors[i]["token_literal"] != actual_errors[i].token.literal:
                ok = False
                tracker.add_error_message(
                    f"Expected error literal: {test_case_errors[i]['token_literal']}, but found {actual_errors[i].token.literal}"
                )
            if test_case_errors[i]["line_number"] != actual_errors[i].token.line_number:
                ok = False
                tracker.add_error_message(
                    f"Expected error line number: {test_case_errors[i]['line_number']}, but found {actual_errors[i].token.line_number}"
                )
            if test_case_errors[i]["column"] != actual_errors[i].token.column_number:
                ok = False
                tracker.add_error_message(
                    f"Expected error column number: {test_case_errors[i]['column']}, but found {actual_errors[i].token.column_number}"
                )
            if test_case_errors[i]["message"] != actual_errors[i].message:
                ok = False
                tracker.add_error_message(
                    f"Expected error message: {test_case_errors[i]['message']}, but found {actual_errors[i].message}"
                )

            if ok:
                tracker.inc_success()



TEST_FILES = [
    {
        "general_component": "parser_source collection tests",
        "test_manifest_file": "../TestFiles/FullParserTests/module_collection_tests.json"
    }
]