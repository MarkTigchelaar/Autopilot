from Testing.progress_tracker import ProgressTracker
from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.ExternalStatementParsing.module_parsing import parse_module

def test_module_statement_parser(progress_tracker: ProgressTracker):
    error_tests = open_json(
        "Testing/Parsing/ExternalStatementTests/ModuleStatementParsing/module_statement_parsing_tests.json"
    )
    test_case_folder = "Testing/Parsing/ExternalStatementTests/ModuleStatementParsing/"
    print("Running module statement parsing tests")
    run_tests(
        error_tests, test_case_folder, "TestCases", "AstFiles", progress_tracker, parse_module
    )
