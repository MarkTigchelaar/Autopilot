from Testing.progress_tracker import ProgressTracker

from Testing.SemanticAnalysis.ImportsAndModules.ModuleUniqueness.module_uniqueness_tests import run_module_uniqueness_tests
from Testing.SemanticAnalysis.ImportsAndModules.ImportTests.import_tests import run_import_tests
from Testing.SemanticAnalysis.ImportsAndModules.ModuleDependencyGraphs.test_module_dependency_graphs import run_module_dependency_tests
from Testing.SemanticAnalysis.LocalAnalysis.test_local_analysis import run_local_analysis_tests
from Testing.SemanticAnalysis.ModuleAnalysis.test_module_analysis import run_module_analysis_tests
from Testing.SemanticAnalysis.GlobalAnalysis.ImportTests.import_item_existence import run_import_item_existence_tests
from Testing.SemanticAnalysis.GlobalAnalysis.TypeResolution.test_type_resolver import run_type_setting_tests


def run_semantic_analysis_tests(progress_tracker: ProgressTracker) -> None:
    # run_module_uniqueness_tests(progress_tracker)
    # run_import_tests(progress_tracker)
    # run_module_dependency_tests(progress_tracker)
    # run_local_analysis_tests(progress_tracker)
    # run_module_analysis_tests(progress_tracker)
    # run_import_item_existence_tests(progress_tracker)
    run_type_setting_tests(progress_tracker)