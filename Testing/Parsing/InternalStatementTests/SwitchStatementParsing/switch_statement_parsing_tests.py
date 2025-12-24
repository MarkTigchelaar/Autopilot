from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.InternalStatementParsing.switch_parsing import parse_switch


def test_switch_statement_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/InternalStatementTests/SwitchStatementParsing/switch_statement_parsing_tests.json"
    )
    test_case_folder = (
        "Testing/Parsing/InternalStatementTests/SwitchStatementParsing/"
    )
    print("Running switch statement parsing tests")
    run_tests(
        error_tests,
        test_case_folder,
        "TestCases",
        "AstFiles",
        progress_tracker,
        parse_switch,
    )
