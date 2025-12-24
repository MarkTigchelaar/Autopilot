from Testing.progress_tracker import ProgressTracker
from Testing.utils import (
    open_json,
    run_tests,
)
from Parsing.source_file_parsing import parse_file


def test_source_file_parser(progress_tracker: ProgressTracker) -> None:
    error_tests = open_json(
        "Testing/Parsing/SourceFileParsing/source_file_parsing_tests.json"
    )
    test_case_folder = "Testing/Parsing/SourceFileParsing/"
    print("Running source file parsing tests")
    run_tests(
        error_tests,
        test_case_folder,
        "TestCases",
        "AstFiles",
        progress_tracker,
        parse_file,
        False,
    )
