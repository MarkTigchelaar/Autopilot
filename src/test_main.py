import os
import time

from TestingComponents.testing_utilities import get_json_from_file
from TestingComponents.progress_tracker import ProgressTracker

from TestingComponents.phase_one_tests import phase_one_tests
from TestingComponents.phase_two_tests import phase_two_tests
from TestingComponents.phase_three_tests import phase_three_tests
from TestingComponents.phase_four_tests import phase_four_tests
from TestingComponents.phase_five_tests import phase_five_tests

TEST_MANIFEST_ONE = "../TestFiles/tokenizer_parser_test_manifest.json"
TEST_MANIFEST_TWO = "../TestFiles/local_semantic_analysis_test_manifest.json"
TEST_MANIFEST_THREE = "../TestFiles/analysis_table_test_manifest.json"
TEST_MANIFEST_FOUR = "../TestFiles/global_semantic_analysis_manifest.json"
TEST_MANIFEST_FIVE = "../TestFiles/global_statement_analysis_manifest.json"

def main():
    current_dir = os.path.dirname(__file__)
    tracker = ProgressTracker()

    print("Begin tests!")
    start_time = time.time()
    # abs_file_path = current_dir + '/' + TEST_MANIFEST_ONE
    # test_json = get_json_from_file(abs_file_path)
    # phase_one_tests(tracker, test_json, current_dir)

    # abs_file_path = current_dir + '/' + TEST_MANIFEST_TWO
    # test_json = get_json_from_file(abs_file_path)
    # phase_two_tests(tracker, test_json, current_dir)

    # abs_file_path = current_dir + '/' + TEST_MANIFEST_THREE
    # test_json = get_json_from_file(abs_file_path)
    # phase_three_tests(tracker, test_json, current_dir)

    # abs_file_path = current_dir + '/' + TEST_MANIFEST_FOUR
    # test_json = get_json_from_file(abs_file_path)
    # phase_four_tests(tracker, test_json, current_dir)

    abs_file_path = current_dir + '/' + TEST_MANIFEST_FIVE
    test_json = get_json_from_file(abs_file_path)
    phase_five_tests(tracker, test_json, current_dir)

    
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
    print(f"Tests took {elapsed_time / 60.0} minutes")


if __name__ == '__main__':
    main()
