from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.InternalStatementParsing.continue_parsing import parse_continue

def test_continue_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/InternalStatementTests/ContinueStatementParsing/continue_statement_parsing_tests.json"
    )
    test_case_folder = "Testing/Parsing/InternalStatementTests/ContinueStatementParsing/"
    print("Running continue statement parsing tests")
    run_tests(
        error_tests, test_case_folder, "TestCases", "AstFiles", progress_tracker, parse_continue
    )
