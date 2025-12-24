import time
import os
from Testing.Tokenization.tokenizer_tests import run_tokenization_tests
from Testing.Parsing.parsing_tests import run_parsing_tests
from Testing.SemanticAnalysis.semantic_analysis_tests import run_semantic_analysis_tests
from Testing.progress_tracker import ProgressTracker


def main():
    progress_tracker = ProgressTracker()
    start_time = time.time()


    # run_tokenization_tests(progress_tracker)
    # run_parsing_tests(progress_tracker)
    run_semantic_analysis_tests(progress_tracker)
    elapsed_time = time.time() - start_time

    report_progress(progress_tracker)

    print(f"Tests took {elapsed_time // 60} minutes, {elapsed_time % 60.0} seconds")






def report_progress(progress_tracker: ProgressTracker) -> None:
    print("End result: " + progress_tracker.get_results())
    err_file = "./failed_tests.txt"
    if progress_tracker.no_failures():
        try:
            os.remove(err_file)
        except FileNotFoundError:
            print("No errors in compiler reported")
    else:
        failurelog = open(err_file, "w")
        for err in progress_tracker.get_error_messages():
            failurelog.write(err + "\n")
        failurelog.close()
        print("Errors printed out to " + err_file)


if __name__ == "__main__":
    main()
