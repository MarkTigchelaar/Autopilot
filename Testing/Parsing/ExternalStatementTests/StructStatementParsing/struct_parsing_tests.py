from Testing.progress_tracker import ProgressTracker
from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.ExternalStatementParsing.struct_parsing import parse_struct



def test_struct_statement_parser(progress_tracker: ProgressTracker):
    error_tests = open_json(
        "Testing/Parsing/ExternalStatementTests/StructStatementParsing/struct_statement_parsing_tests.json"
    )
    test_case_folder = "Testing/Parsing/ExternalStatementTests/StructStatementParsing/"
    print("Running struct statement parsing tests")
    run_tests(
        error_tests, test_case_folder, "TestCases", "AstFiles", progress_tracker, parse_struct, False
    )