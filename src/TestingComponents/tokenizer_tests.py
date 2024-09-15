from Tokenization.tokenizer import Tokenizer
from ErrorHandling.error_manager import ErrorManager
from TestingComponents.testing_utilities import record_component_test, record_component_test_str
import symbols


def call_tokenizer_tests(tests: dict, tracker, current_dir: str) -> None:
    print("Testing Tokenizer...")
    for test in tests:
        err_manager = ErrorManager()
        toks = Tokenizer(err_manager)
        tokenizer_test(toks, test, tracker, current_dir, err_manager)
    print("Done test for Tokenizer\n")


def tokenizer_test(
    tokenizer: Tokenizer,
    test: dict,
    tracker,
    current_dir: str,
    err_manager: ErrorManager,
) -> None:
    tokenizer.load_src(current_dir + "/" + test["file"])

    expected = test["expected_literal"]
    lines = test["line_numbers"]
    token_types = test["token_types"]

    i = 0
    while tokenizer.has_tokens():
        token = tokenizer.next_token()

        if "error" in test:
            i += 1
            err = test["error"]
            error = err_manager.next_tokenizer_error()
            tok_error = error.token
            record_component_test_str(test, tracker, err["file"], tok_error.file_name)
            record_component_test(test, tracker, err["line"], tok_error.line_number)
            record_component_test(test, tracker, err["column"], tok_error.column_number)
            record_component_test(test, tracker, err["message"], error.message)
            continue
        elif i >= len(expected):
            break

        if err_manager.has_errors():
            tok_err = err_manager.next_tokenizer_error()
            record_component_test(test, tracker, "ok", tok_err)
            print(
                "ERROR: tests expected no errors, but Tokenizer generated errors! See error file."
            )

        record_component_test(test, tracker, expected[i], token.literal)
        record_component_test(test, tracker, lines[i], token.line_number)
        record_component_test(test, tracker, token_types[i], token.type_symbol)

        i += 1

    eof_token = tokenizer.next_token()
    if tokenizer.has_tokens():
        raise Exception("Still has tokens?")
    if eof_token.type_symbol != symbols.EOF:
        raise Exception("Did not encounter eof token")
    if eof_token.literal != "":
        raise Exception("eof token contains a literal")
    if eof_token.line_number == None:
        raise Exception("eof token does not contain a line number")
