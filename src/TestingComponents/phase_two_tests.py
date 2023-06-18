from SemanticAnalysis.semantic_analyzer import SemanticAnalyzer
from Parsing.parse import parse_src
from driver import Driver
from TestingComponents.testing_utilities import get_json_from_file, call_local_semantic_tests

def phase_two_tests(tracker, test_json, current_dir):
    print("\n\n\n Local Semantic Analysis Tests:\n")
    for test in test_json:
        component_tests = get_json_from_file(current_dir + "/" + test["test_manifest_file"])

        general_component = test["general_component"]
        print(general_component)
        # if "generated" in general_component:
        #     continue
        call_local_semantic_tests(component_tests, tracker, current_dir, semantic_test, general_component)

def semantic_test(tokenizer, err_manager):
    analyzer = SemanticAnalyzer(err_manager)
    driver = BypassSaveDriver(tokenizer, err_manager, analyzer)
    parse_src(driver)

class BypassSaveDriver(Driver):
    def analyze_locally(self, analysis_fn, save_fn, root_node):
        if root_node is None:
            return
        analysis_fn(self.analyzer, root_node)
        #save_fn(self.analyzer, root_node)