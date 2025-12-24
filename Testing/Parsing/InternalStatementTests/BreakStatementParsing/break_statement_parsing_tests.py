from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.InternalStatementParsing.break_parsing import parse_break



def test_break_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/InternalStatementTests/BreakStatementParsing/break_statement_parsing_tests.json"
    )
    test_case_folder = "Testing/Parsing/InternalStatementTests/BreakStatementParsing/"
    print("Running break statement parsing tests")
    run_tests(
        error_tests, test_case_folder, "TestCases", "AstFiles", progress_tracker, parse_break
    )
