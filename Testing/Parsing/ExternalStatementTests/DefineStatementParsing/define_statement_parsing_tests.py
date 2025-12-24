from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.ExternalStatementParsing.define_parsing import parse_define

def test_define_statement_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/ExternalStatementTests/DefineStatementParsing/define_statement_parsing_tests.json"
    )
    test_case_folder = "Testing/Parsing/ExternalStatementTests/DefineStatementParsing/"
    print("Running define statement parsing tests")
    run_tests(
        error_tests, test_case_folder, "TestCases", "AstFiles", progress_tracker, parse_define
    )
