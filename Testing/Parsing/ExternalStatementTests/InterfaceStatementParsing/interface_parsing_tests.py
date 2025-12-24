from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.ExternalStatementParsing.interface_parsing import parse_interface


def test_interface_statement_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/ExternalStatementTests/InterfaceStatementParsing/interface_statement_parsing_tests.json"
    )
    test_case_folder = (
        "Testing/Parsing/ExternalStatementTests/InterfaceStatementParsing/"
    )
    print("Running interface sequence parsing tests")
    run_tests(
        error_tests,
        test_case_folder,
        "TestCases",
        "AstFiles",
        progress_tracker,
        parse_interface,
        False
    )
