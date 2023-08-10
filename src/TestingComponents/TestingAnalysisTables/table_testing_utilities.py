import json
from Tokenization.tokenizer import Tokenizer
from ErrorHandling.error_manager import ErrorManager
import symbols
import random

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
        database = None
        #semantic_test(tok, err_manager)
        try:
            database = semantic_test(tok, err_manager)
        except Exception as e:
            print("EXCEPTION in file: " + test_case["file"] + ":\n" + str(e))
            record_component_test(test_case, tracker, "OK", "EXCEPTION: " + str(e))
            continue
        tok.close_src()
        if database is None:
            raise Exception("INTERNAL ERROR: Databse was not returned by semantic test function")
        
        # check for errors
        # retrieve needed tables
        # for each check id, and data against test case
        if err_manager.has_errors() and test_case["errors"] is None:
            print("ERROR: tests expected no errors, but parsing generated errors! See error file.")
            while err_manager.has_errors():
                err = err_manager.next_error()
                record_component_test(test_case, tracker, "ok", err.message + ": " + err.token.to_string())
        elif not err_manager.has_errors() and test_case["errors"] is not None:
            print("ERROR: tests expected errors, but parsing generated no errors! See error file.")
            record_component_test(test_case, tracker, "error", "ok")
        else:
            run_table_comparisons(database, test_case, tracker)


def get_msg(expect: str, actual: str) -> str:
    return " expected: \"" + str(expect) + "\", got \"" + str(actual) + "\""


def record_component_test(test_case: dict, tracker, expected: str, result: str) -> None:
    if str(result) != str(expected):
        msg = FAILURE + "In " + test_case["file"] + ":\n" + get_msg(expected, result)
        tracker.add_error_message(msg + "\n\n")
    else:
        tracker.inc_success()


def run_table_comparisons(database, test_case, tracker):
    object_count_compare(database, test_case, tracker)
    involved_table_check(database, test_case, tracker)
    check_table_contents(database, test_case, tracker)


def object_count_compare(database, test_case, tracker):
    number_of_objects = len(database.objects)
    expected_number_of_objects = test_case["object_count"]
    record_component_test(test_case, tracker, number_of_objects, expected_number_of_objects)


def involved_table_check(database, test_case, tracker):
    expected_tables = list(test_case["tables"].keys())
    for table in database.tables:
        if table in expected_tables:
            record_component_test(test_case, tracker, True, database.get_table(table).has_contents())
        else:
            record_component_test(test_case, tracker, False, database.get_table(table).has_contents())

# modules
# files
# typenames
def check_table_contents(database, test_case, tracker):
    expected_tables = list(test_case["tables"].keys())
    # Just to prove that these tests do not require a certain order.
    random.shuffle(expected_tables)

    for table_name in expected_tables:
        table = database.get_table(table_name)
        test_table = test_case["tables"][table_name]
        query_runner = table_tester_factory(table_name)
        query_runner.set_table(table)
        for row in test_table:
            record_component_test(test_case, tracker, True, query_runner.row_is_defined(row))



def table_tester_factory(table_name):
    tester = None
    match table_name:
        case "modules":
            tester = ModuleTableTestQueryRunner()
        case "files":
            tester = FilesTableTestQueryRunner()
        case "typenames":
            tester = TypenamesTableTestQueryRunner()
        case _:
            raise Exception(f"INTERNAL ERROR: table tester for table {table_name} not found")
    return tester



class TestQueryRunner:
    def __init__(self) -> None:
        self.table = None
    
    def set_table(self, table):
        self.table = table
    
    def row_is_defined(self, _):
        raise Exception("Not implemented")

class ModuleTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, row):
        return self.table.is_module_defined(row["name"])


class FilesTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, row):
        pass

class TypenamesTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, row):
        pass