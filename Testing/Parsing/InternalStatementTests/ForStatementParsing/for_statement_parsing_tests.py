from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.InternalStatementParsing.for_parsing import parse_for


def test_for_statement_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/InternalStatementTests/ForStatementParsing/for_statement_parsing_tests.json"
    )
    test_case_folder = (
        "Testing/Parsing/InternalStatementTests/ForStatementParsing/"
    )
    print("Running for statement parsing tests")
    run_tests(
        error_tests,
        test_case_folder,
        "TestCases",
        "AstFiles",
        progress_tracker,
        parse_for,
    )
