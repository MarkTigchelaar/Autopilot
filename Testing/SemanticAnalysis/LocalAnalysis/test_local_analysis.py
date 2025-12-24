from Testing.progress_tracker import ProgressTracker
from Testing.utils import (
    open_json,
    object_to_json,
    local_semantic_analysis_setup,
    check_errors_as_json,
)
from ErrorHandling.semantic_error_manager import SemanticErrorManager

from Parsing.ExternalStatementParsing.enum_parsing import parse_enum
from SemanticAnalysis.LocalAnalysis.enum_analysis import analyze_enum
from Parsing.ExternalStatementParsing.error_parsing import parse_error
from SemanticAnalysis.LocalAnalysis.error_analysis import analyze_error
from Parsing.ExternalStatementParsing.union_parsing import parse_union
from SemanticAnalysis.LocalAnalysis.union_analysis import analyze_union
from Parsing.ExternalStatementParsing.import_parsing import parse_import
from SemanticAnalysis.LocalAnalysis.import_analysis import analyze_import
from Parsing.ExternalStatementParsing.define_parsing import parse_define
from SemanticAnalysis.LocalAnalysis.define_analysis import analyze_define
from Parsing.ExternalStatementParsing.interface_parsing import parse_interface
from SemanticAnalysis.LocalAnalysis.interface_analysis import analyze_interface
from Parsing.ExternalStatementParsing.function_parsing import parse_function
from SemanticAnalysis.LocalAnalysis.function_analysis import (
    analyze_arg_names,
    analyze_variable_declarations,
    analyze_variable_usage,
    analyze_let_variable_reassignment,
    analyze_loop_branching_and_labels,
    check_return_value_validity,
    analyze_return_paths,
)
from Parsing.ExternalStatementParsing.struct_parsing import parse_struct
from SemanticAnalysis.LocalAnalysis.struct_analysis import analyze_struct
from Parsing.source_file_parsing import parse_file


def testing_parse_file(driver):
    ast_list = parse_file(driver)
    return ast_list[0]


def run_local_analysis_tests(progress_tracker: ProgressTracker) -> None:
    run_test("EnumTests", "enum_tests.json", parse_enum, analyze_enum, progress_tracker)
    run_test(
        "ErrorTests", "error_tests.json", parse_error, analyze_error, progress_tracker
    )
    run_test(
        "UnionTests", "union_tests.json", parse_union, analyze_union, progress_tracker
    )
    run_test(
        "ImportTests",
        "import_tests.json",
        parse_import,
        analyze_import,
        progress_tracker,
    )
    run_test(
        "DefineTests",
        "define_tests.json",
        parse_define,
        analyze_define,
        progress_tracker,
    )
    run_test(
        "InterfaceTests",
        "interface_tests.json",
        parse_interface,
        analyze_interface,
        progress_tracker,
    )
    run_test(
        "FunctionArgumentTests",
        "tests.json",
        parse_function,
        analyze_arg_names,
        progress_tracker,
        False,
    )
    run_test(
        "FunctionVariableDeclarationTests",
        "tests.json",
        parse_function,
        analyze_variable_declarations,
        progress_tracker,
        False,
    )
    run_test(
        "FunctionVariableUsageTests",
        "tests.json",
        parse_function,
        analyze_variable_usage,
        progress_tracker,
        False,
    )
    run_test(
        "LoopLabelAndControlTests",
        "loop_label_and_control_tests.json",
        parse_function,
        analyze_loop_branching_and_labels,
        progress_tracker,
        False,
    )
    run_test(
        "FunctionReturnTypeTests",
        "tests.json",
        parse_function,
        check_return_value_validity,
        progress_tracker,
        False,
    )
    run_test(
        "StructTests",
        "tests.json",
        parse_struct,
        analyze_struct,
        progress_tracker,
        False,
    )
    run_test(
        "FunctionReturnPathTests",
        "tests.json",
        parse_function,
        analyze_return_paths,
        progress_tracker,
        False,
    )
    run_test(
        "FunctionBulkReturnPathTests",
        "tests.json",
        testing_parse_file,
        analyze_return_paths,
        progress_tracker,
        False,
    )
    run_test(
        "FunctionLetVariableReAssignmentTests",
        "tests.json",
        parse_function,
        analyze_let_variable_reassignment,
        progress_tracker,
        False,
    )


def get_test_case_folder(test_folder):
    import os

    return f"{os.getcwd()}/Testing/SemanticAnalysis/LocalAnalysis/{test_folder}/"


def get_tests(test_folder, json_file_name):
    return open_json(test_folder + json_file_name)


def run_test(
    test_type_folder,
    test_manifest_name,
    parse_function,
    analysis_function,
    progress_tracker,
    is_unit_testing=True,
):
    test_folder_path = get_test_case_folder(test_type_folder)
    tests = get_tests(test_folder_path, test_manifest_name)
    test_case_folder_path = test_folder_path + "TestCases/"
    for test in tests:
        ast, full_file_path = local_semantic_analysis_setup(
            test_case_folder_path, test, parse_function, is_unit_testing
        )
        error_manager = SemanticErrorManager()
        analysis_function(error_manager, ast)

        if test["errors"] is None:
            test["errors"] = []
        actual_errors = object_to_json(error_manager.get_errors())
        check_errors_as_json(
            actual_errors,
            test["errors"],
            test,
            test_case_folder_path.rstrip("/"),
            progress_tracker,
        )
