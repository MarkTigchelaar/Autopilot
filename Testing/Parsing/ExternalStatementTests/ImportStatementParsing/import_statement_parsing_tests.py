from Testing.progress_tracker import ProgressTracker

from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.ExternalStatementParsing.import_parsing import parse_import


def test_import_statement_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/ExternalStatementTests/ImportStatementParsing/import_statement_parsing_tests.json"
    )
    test_case_folder = "Testing/Parsing/ExternalStatementTests/ImportStatementParsing/"
    print("Running import statement parsing tests")
    run_tests(
        error_tests, test_case_folder, "TestCases", "AstFiles", progress_tracker, parse_import
    )
