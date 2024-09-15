from SemanticAnalysis.semantic_analyzer import SemanticAnalyzer
from Parsing.parse import parse_src
from driver import Driver
from TestingComponents.testing_utilities import (
    get_json_from_file,
    call_local_semantic_tests,
)


def semantic_test(tokenizer, err_manager):
    analyzer = SemanticAnalyzer(err_manager)
    driver = BypassSaveDriver(tokenizer, err_manager, analyzer)
    parse_src(driver)


class BypassSaveDriver(Driver):
    def analyze_locally(self, analysis_fn, save_fn, root_node):
        if root_node is None:
            return
        analysis_fn(self.analyzer, root_node)


def local_semantic_analysis_checks(tracker, current_dir):
    print("Local Semantic Analysis Tests:\n")
    for test in TEST_JSON:
        component_tests = get_json_from_file(
            current_dir + "/" + test["test_manifest_file"]
        )
        general_component = test["general_component"]
        # if general_component == "generated_function_return_paths":
        #     continue
        call_local_semantic_tests(
            component_tests, tracker, semantic_test, general_component
        )


TEST_JSON = [
    {
        "general_component": "enum",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/enum_analysis_tests.json",
    },
    {
        "general_component": "error",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/error_analysis_tests.json",
    },
    {
        "general_component": "union",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/union_analysis_tests.json",
    },
    {
        "general_component": "import",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/import_analysis_tests.json",
    },
    {
        "general_component": "module",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/module_analysis_tests.json",
    },
    {
        "general_component": "define",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/define_analysis_tests.json",
    },
    {
        "general_component": "interface",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/interface_analysis_tests.json",
    },
    {
        "general_component": "function_arg_types",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/function_arg_type_tests.json",
    },
    {
        "general_component": "structs",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/struct_analysis_tests.json",
    },
    {
        "general_component": "loop_label_and_logic_check",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/loop_label_and_logic_tests.json",
    },
    {
        "general_component": "function_return_paths",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/function_return_paths_tests.json",
    },
    {
        "general_component": "generated_function_return_paths",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/function_return_paths_generated_tests.json",
    },
    {
        "general_component": "declaration_checks",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/function_variable_declaration_tests.json",
    },
    {
        "general_component": "variable_definition_checks",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/function_variable_definition_tests.json",
    },
]
