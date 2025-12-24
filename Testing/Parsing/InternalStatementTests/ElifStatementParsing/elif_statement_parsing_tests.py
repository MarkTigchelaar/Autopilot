from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.InternalStatementParsing.elif_parsing import parse_elif

def test_elif_statement_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/InternalStatementTests/ElifStatementParsing/elif_statement_parsing_tests.json"
    )
    test_case_folder = "Testing/Parsing/InternalStatementTests/ElifStatementParsing/"
    print("Running elif statement parsing tests")
    run_tests(
        error_tests, test_case_folder, "TestCases", "AstFiles", progress_tracker, parse_elif
    )