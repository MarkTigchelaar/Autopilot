from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.InternalStatementParsing.re_assignment_or_call_parsing import parse_re_assignment_or_call


def test_reassign_statement_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/InternalStatementTests/ReassignOrCallStatementParsing/reassign_or_call_statement_parsing_tests.json"
    )
    test_case_folder = (
        "Testing/Parsing/InternalStatementTests/ReassignOrCallStatementParsing/"
    )
    print("Running re - assign or call statement parsing tests")
    run_tests(
        error_tests,
        test_case_folder,
        "TestCases",
        "AstFiles",
        progress_tracker,
        parse_re_assignment_or_call,
    )
