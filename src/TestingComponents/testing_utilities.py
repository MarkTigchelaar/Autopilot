import json
from Tokenization.tokenizer import Tokenizer
from ErrorHandling.error_manager import ErrorManager
import symbols

FAILURE = "TEST CASE FAILURE,"


def get_json_from_file(manifest: str):
    jsonfile = open(manifest, "r")
    tests = json.load(jsonfile)
    jsonfile.close()
    return tests


def write_json_to_file(filename, output):
    json_object = json.dumps(output, indent=4)

    # Writing to sample.json
    with open(filename + ".json", "w") as outfile:
        outfile.write(json_object)


def get_msg(expect: str, actual: str) -> str:
    return ' expected: "' + str(expect) + '", got "' + str(actual) + '"'


def printErrors(reportedErrors: dict) -> None:
    for err in reportedErrors:
        print("file name: " + err["file"])
        print("token literal: " + err["tokenLiteral"])
        print("line number: " + err["lineNumber"])
        print("message: " + err["message"])


def record_component_test(test_case: dict, tracker, expected: str, result: str) -> None:
    if str(result) != str(expected):
        msg = FAILURE + "In " + test_case["file"] + ":\n" + get_msg(expected, result)
        tracker.add_error_message(msg + "\n\n")
    else:
        tracker.inc_success()


def record_component_test_str(
    test_case: dict, tracker, expected: str, result: str
) -> None:
    if str(result) not in str(expected) and str(expected) not in str(result):
        msg = FAILURE + "In " + test_case["file"] + ":\n" + get_msg(expected, result)
        tracker.add_error_message(msg + "\n\n")
    else:
        tracker.inc_success()


def token_to_json(token) -> dict:
    if token is None:
        return dict()
    return {
        "literal": token.literal or "null",
        "type": token.type_symbol or "null",
        "line_number": token.line_number or "null",
        "column_number": token.column_number or "null",
    }


def call_parsing_tests(
    component_tests, tracker, current_dir, parse_test_fn, component_name
):
    print("Testing " + component_name + " parsing...")
    for test in component_tests:
        err_manager = ErrorManager()
        tok = Tokenizer(err_manager)

        try:
            tok.load_src(test["file"])
        except:
            tok.load_src(current_dir + "/" + test["file"])
        ast = parse_test_fn(tok, err_manager)

        tok.close_src()
        if err_manager.has_errors() and test["errors"] is None:
            print(
                "ERROR: tests expected no errors, but parsing generated errors! See error file."
            )
            while err_manager.has_errors():
                err = err_manager.next_error()
                record_component_test(
                    test, tracker, "ok", err.message + ": " + err.token.to_string()
                )

        elif not err_manager.has_errors() and test["errors"] is not None:
            print(
                "ERROR: tests expected errors, but parsing generated no errors! See error file."
            )
            record_component_test(test, tracker, "error", "ok")

        elif err_manager.has_errors() and test["errors"] is not None:
            for err in test["errors"]:
                try:
                    parse_err = err_manager.next_parser_error()
                except:
                    parse_err = err_manager.next_tokenizer_error()
                record_component_test(
                    test, tracker, err["file"], parse_err.token.file_name
                )
                record_component_test(
                    test, tracker, err["tokenLiteral"], parse_err.token.literal
                )
                record_component_test(
                    test, tracker, err["lineNumber"], parse_err.token.line_number
                )
                record_component_test(test, tracker, err["message"], parse_err.message)

                # column number added to parsing later,
                # previous tests don't have that data
                if "column_number" in err and err["column_number"]:
                    record_component_test(
                        test,
                        tracker,
                        err["column_number"],
                        parse_err.token.column_number,
                    )
            if err_manager.has_errors():
                while err_manager.has_errors():
                    parse_err = err_manager.next_parser_error()
                record_component_test(test, tracker, "BLANK", parse_err.message)
        elif "ast" in test:
            ast_test(ast, test, err_manager, tracker)

        else:
            ast_string_list = list()
            ast_type_list = list()
            ast.print_literal(ast_string_list)
            ast_string = "".join(ast_string_list)
            record_component_test(test, tracker, test["astString"], ast_string)

            ast.print_token_types(ast_type_list)
            ast_type_string = "".join(ast_type_list).rstrip(" ")
            record_component_test(
                test, tracker, test["tokenTypeString"], ast_type_string
            )


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


def ast_test(ast, test, err_manager, tracker):
    # shouldn't ever have errors if this code is reached
    if err_manager.has_errors():
        print("has errors")
    expected_ast = test["ast"]
    ast_json = list()
    for node in ast:
        json_node = node.to_json()
        ast_json.append(json_node)
    # record_component_test(test, tracker, test["astString"], ast_string)
    compare_asts(ast_json, expected_ast, test, tracker)


def compare_asts(ast_json, expected_ast, test, tracker):
    if expected_ast is None or ast_json is None:
        record_component_test(test, tracker, str(expected_ast), str(ast_json))
        return
    if type(expected_ast) is dict:
        for key in expected_ast:
            if key not in ast_json:
                record_component_test(
                    test,
                    tracker,
                    ",".join(list(expected_ast.keys())),
                    ",".join(list(ast_json.keys())),
                )
                return
            else:
                compare_asts(ast_json[key], expected_ast[key], test, tracker)
        if len(ast_json.keys()) > len(expected_ast.keys()):
            record_component_test(
                test,
                tracker,
                ",".join(list(expected_ast.keys())),
                ",".join(list(ast_json.keys())),
            )
    elif type(expected_ast) is list:
        if len(ast_json) == len(expected_ast):
            for i in range(len(expected_ast)):
                compare_asts(ast_json[i], expected_ast[i], test, tracker)
        else:
            record_component_test(
                test, tracker, json.dumps(expected_ast), json.dumps(ast_json)
            )
    else:
        record_component_test(test, tracker, expected_ast, ast_json)


def parser_happy_path_tests(test_list, tracker, parse_test_fn, current_dir):
    print("happy path tests")
    for i, test in enumerate(test_list):
        print("running happy path test " + str(i + 1))
        err_manager = ErrorManager()
        tok = Tokenizer(err_manager)
        try:
            tok.load_src(test["file"])
        except:
            tok.load_src(current_dir + "/" + test["file"])
        try:
            _ = parse_test_fn(tok, err_manager)
        except Exception as e:
            print("EXCEPTION in file: " + test["file"] + ":\n" + str(e))
            record_component_test(test, tracker, "OK", "EXCEPTION: " + str(e))
            continue

        if err_manager.has_errors():
            print("Errors found! Should have 0 errors")
            while err_manager.has_errors():
                err = err_manager.next_error()
                record_component_test(
                    test, tracker, "ok", err.message + ": " + err.token.to_string()
                )
        else:
            record_component_test(test, tracker, "ok", "ok")


def call_local_semantic_tests(
    component_tests, tracker, current_dir, test_fn, component_name
):
    print("Testing local semantic analysis for " + component_name + "...")
    for test_case in component_tests:
        err_manager = ErrorManager()
        tok = Tokenizer(err_manager)

        try:
            tok.load_src(test_case["file"])
        except:
            tok.load_src(current_dir + "/" + test_case["file"])
        try:
            test_fn(tok, err_manager)
        except Exception as e:
            print("EXCEPTION in file: " + test_case["file"] + ":\n" + str(e))
            record_component_test(test_case, tracker, "OK", "EXCEPTION: " + str(e))
            continue
        tok.close_src()

        if not err_manager.has_errors(True) and test_case["errors"] is None:
            tracker.inc_success()
        if err_manager.has_errors(True) and test_case["errors"] is None:
            print(
                "ERROR: tests expected no errors, but analysis generated errors! See error file."
            )
            while err_manager.has_errors(True):
                err = err_manager.next_error()
                record_component_test(
                    test_case, tracker, "ok", err.message + ": " + err.token.to_string()
                )

        elif not err_manager.has_errors(True) and test_case["errors"] is not None:
            print(
                "ERROR: tests expected errors, but analysis generated no errors! See error file."
            )
            record_component_test(test_case, tracker, "error", "ok")

        elif err_manager.has_errors(True) and test_case["errors"] is not None:
            for err in test_case["errors"]:
                try:
                    error = err_manager.next_semantic_error()
                except:
                    error = err_manager.next_parser_error()
                record_component_test_str(
                    test_case, tracker, err["file"], error.token.file_name
                )
                record_component_test(
                    test_case, tracker, err["tokenLiteral"], error.token.literal
                )
                record_component_test(
                    test_case, tracker, err["lineNumber"], error.token.line_number
                )
                record_component_test(test_case, tracker, err["message"], error.message)

                # column number added to parsing later,
                # previous tests don't have that data
                if "column_number" in err and err["column_number"]:
                    record_component_test(
                        test_case,
                        tracker,
                        err["column_number"],
                        error.token.column_number,
                    )
            while err_manager.has_errors(True):
                err = err_manager.next_error()
                record_component_test(test_case, tracker, "BLANK", err.message)
