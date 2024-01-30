from SemanticAnalysis.semantic_analyzer import SemanticAnalyzer
from Parsing.parse import parse_src
from driver import Driver
from TestingComponents.testing_utilities import get_json_from_file
from TestingComponents.TestingAnalysisTables.table_testing_utilities import (
    table_load_tests,
)


def phase_three_tests(tracker, test_json, current_dir):
    print("Phase 3 tests")
    for test in test_json:
        component_tests = get_json_from_file(
            current_dir + "/" + test["test_manifest_file"]
        )
        general_component = test["general_component"]
        print(general_component)
        table_load_tests(
            component_tests, tracker, current_dir, semantic_test, general_component
        )


def semantic_test(tokenizer, err_manager, database=None):
    analyzer = SemanticAnalyzer(err_manager, database)
    driver = Driver(tokenizer, err_manager, analyzer)
    parse_src(driver)
    return analyzer.database
