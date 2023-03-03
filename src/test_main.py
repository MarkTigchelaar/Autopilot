import os

from TestingComponents.phase_one_tests import phase_one_tests
from TestingComponents.testing_utilities import get_json_from_file
from TestingComponents.progress_tracker import ProgressTracker
from TestingComponents.phase_two_tests import phase_two_tests

TEST_MANIFEST_ONE = "../TestFiles/tokenizer_parser_test_manifest.json"
TEST_MANIFEST_TWO = "../TestFiles/semantic_analysis_test_manifest.json"

def main():
    current_dir = os.path.dirname(__file__)
    tracker = ProgressTracker()

    abs_file_path = current_dir + '/' + TEST_MANIFEST_ONE
    test_json = get_json_from_file(abs_file_path)
    phase_one_tests(tracker, test_json, current_dir)

    abs_file_path = current_dir + '/' + TEST_MANIFEST_TWO
    test_json = get_json_from_file(abs_file_path)
    phase_two_tests(tracker, test_json, current_dir)
    
    print("End result: " + tracker.get_results())
    err_file = "./failed_tests.txt"
    if tracker.no_failures():
        try:
            os.remove(err_file)
        except FileNotFoundError:
            return
    else:
        failurelog = open(err_file, 'w')
        for err in tracker.get_error_messages():
            failurelog.write(err)
        failurelog.close()
        print("Errors printed out to " + err_file)


if __name__ == '__main__':
    main()
