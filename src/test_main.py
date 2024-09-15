import os
import time


from TestingComponents.progress_tracker import ProgressTracker

from TestingComponents.tokenizer_parser_tests import tokenizer_parser_tests
from TestingComponents.local_semantic_analysis_checks import local_semantic_analysis_checks
# from TestingComponents.phase_three_tests import phase_three_tests
from TestingComponents.global_semantic_analysis_checks import global_semantic_analysis_checks
# from TestingComponents.phase_five_tests import phase_five_tests
from TestingComponents.test_full_parser import test_full_parser


# TEST_MANIFEST_THREE = "../TestFiles/analysis_table_test_manifest.json"
# TEST_MANIFEST_FOUR = "../TestFiles/global_semantic_analysis_manifest.json"
# TEST_MANIFEST_FIVE = "../TestFiles/global_statement_analysis_manifest.json"


def main():
    current_dir = os.path.dirname(__file__)
    tracker = ProgressTracker()

    print("Begin tests!")
    start_time = time.time()

    tokenizer_parser_tests(tracker, current_dir)
    local_semantic_analysis_checks(tracker, current_dir)
    global_semantic_analysis_checks(tracker, current_dir)



    test_full_parser(tracker, current_dir)

    
    print("End result: " + tracker.get_results())
    err_file = "./failed_tests.txt"
    if tracker.no_failures():
        try:
            os.remove(err_file)
        except FileNotFoundError:
            print("No errors reported")
    else:
        failurelog = open(err_file, 'w')
        for err in tracker.get_error_messages():
            failurelog.write(err)
        failurelog.close()
        print("Errors printed out to " + err_file)
    
    elapsed_time = time.time() - start_time
    print(f"Tests took {int(elapsed_time / 60)} minutes, {int(elapsed_time) % 60} seconds")


if __name__ == '__main__':
    main()
