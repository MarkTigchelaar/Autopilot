from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.ExternalStatementParsing.unittest_parsing import parse_unittest

def test_unittest_statement_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/ExternalStatementTests/UnittestStatementParsing/unittest_statement_parsing_tests.json"
    )
    test_case_folder = "Testing/Parsing/ExternalStatementTests/UnittestStatementParsing/"
    print("Running unittest statement parsing tests")
    run_tests(
        error_tests, test_case_folder, "TestCases", "AstFiles", progress_tracker, parse_unittest, True
    )
