from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.InternalStatementParsing.unless_parsing import parse_unless


def test_unless_statement_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/InternalStatementTests/UnlessStatementParsing/unless_statement_parsing_tests.json"
    )
    test_case_folder = (
        "Testing/Parsing/InternalStatementTests/UnlessStatementParsing/"
    )
    print("Running unless statement parsing tests")
    run_tests(
        error_tests,
        test_case_folder,
        "TestCases",
        "AstFiles",
        progress_tracker,
        parse_unless,
    )
