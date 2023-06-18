import json
from Tokenization.tokenizer import Tokenizer
from ErrorHandling.error_manager import ErrorManager
import symbols

FAILURE = "TEST CASE FAILURE,"



def table_load_tests(component_tests, tracker, current_dir, semantic_test, component_name):
    print("Testing table loading for " + component_name + "...")
    for test_case in component_tests:
        err_manager = ErrorManager()
        tok = Tokenizer(err_manager)

        try:
            tok.load_src(test_case["file"])
        except:
            tok.load_src(current_dir + "/" + test_case["file"])
        try:
            semantic_test(tok, err_manager)
        except Exception as e:
            print("EXCEPTION in file: " + test_case["file"] + ":\n" + str(e))
            record_component_test(test_case, tracker, "OK", "EXCEPTION: " + str(e))
            continue
        tok.close_src()




def get_msg(expect: str, actual: str) -> str:
    return " expected: \"" + str(expect) + "\", got \"" + str(actual) + "\""



def record_component_test(test_case: dict, tracker, expected: str, result: str) -> None:
    if str(result) != str(expected):
        msg = FAILURE + "In " + test_case["file"] + ":\n" + get_msg(expected, result)
        tracker.add_error_message(msg + "\n\n")
    else:
        tracker.inc_success()