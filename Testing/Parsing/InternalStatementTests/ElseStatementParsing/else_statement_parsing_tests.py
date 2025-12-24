from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.InternalStatementParsing.else_parsing import parse_else

def test_else_statement_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/InternalStatementTests/ElseStatementParsing/else_statement_parsing_tests.json"
    )
    test_case_folder = "Testing/Parsing/InternalStatementTests/ElseStatementParsing/"
    print("Running else statement parsing tests")
    run_tests(
        error_tests, test_case_folder, "TestCases", "AstFiles", progress_tracker, parse_else
    )