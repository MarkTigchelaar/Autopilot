from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.InternalStatementParsing.if_parsing import parse_if

def test_if_statement_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/InternalStatementTests/IfStatementParsing/if_statement_parsing_tests.json"
    )
    test_case_folder = "Testing/Parsing/InternalStatementTests/IfStatementParsing/"
    print("Running if statement parsing tests")
    run_tests(
        error_tests, test_case_folder, "TestCases", "AstFiles", progress_tracker, parse_if
    )