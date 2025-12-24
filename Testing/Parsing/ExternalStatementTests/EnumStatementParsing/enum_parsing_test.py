from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.ExternalStatementParsing.enum_parsing import parse_enum

def test_enum_statement_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/ExternalStatementTests/EnumStatementParsing/enum_statement_parsing_tests.json"
    )
    test_case_folder = "Testing/Parsing/ExternalStatementTests/EnumStatementParsing/"
    print("Running enum statement parsing tests")
    run_tests(
        error_tests, test_case_folder, "TestCases", "AstFiles", progress_tracker, parse_enum
    )
