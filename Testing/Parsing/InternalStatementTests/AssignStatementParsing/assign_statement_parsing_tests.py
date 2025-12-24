from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.InternalStatementParsing.assignment_parsing import parse_assignment


def test_assign_statement_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/InternalStatementTests/AssignStatementParsing/assign_statement_parsing_tests.json"
    )
    test_case_folder = (
        "Testing/Parsing/InternalStatementTests/AssignStatementParsing/"
    )
    print("Running assign statement parsing tests")
    run_tests(
        error_tests,
        test_case_folder,
        "TestCases",
        "AstFiles",
        progress_tracker,
        parse_assignment,
    )
