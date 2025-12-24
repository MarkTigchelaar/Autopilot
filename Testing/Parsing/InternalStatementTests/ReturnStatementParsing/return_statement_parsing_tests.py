from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.InternalStatementParsing.return_parsing import parse_return



def test_return_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/InternalStatementTests/ReturnStatementParsing/return_statement_parsing_tests.json"
    )
    test_case_folder = "Testing/Parsing/InternalStatementTests/ReturnStatementParsing/"
    print("Running return statement parsing tests")
    run_tests(
        error_tests, test_case_folder, "TestCases", "AstFiles", progress_tracker, parse_return
    )
