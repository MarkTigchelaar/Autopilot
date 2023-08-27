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
        
        #tok.remove_path(current_dir)
        database = None
        for i in range(len(test_case["files"])):
            tok = Tokenizer(err_manager)
            try:
                tok.load_src(test_case["files"][i])
            except:
                tok.load_src(current_dir + "/" + test_case["files"][i])
            # current_path = current_dir + "/" + test_case["files"][i]
            # print(f"current path: {current_path}")
            # temp = test_case["files"][i].split("../")
            # temp = temp[1]
            # test_case["files"][i] = "../" + temp
            # current_path = test_case["files"][i]
            # print(f"current path after: {current_path}")


            
            #semantic_test(tok, err_manager)
            try:
                database = semantic_test(tok, err_manager, database)
            except Exception as e:
                print("EXCEPTION in file: " + test_case["files"][i] + ":\n" + str(e))
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
        files = "\n".join([file + "," for file in test_case["files"]])
        msg = FAILURE + "In " + files + ":\n" + get_msg(expected, result)
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
            record_component_test(test_case, tracker, True, query_runner.contents_match(row))



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
    
    def contents_match(self, _):
        raise Exception("Not implemented")

class ModuleTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, row):
        return self.table.is_module_defined(row["name"])
    
    def contents_match(self, row):
        id = self.table.get_module_id_by_name_and_path(row["name"], row["path"])
        if id is None:
            raise Exception("INTERNAL ERROR: module id not found")
        if id != row["object_id"]:
            return False
        table_row = self.table.get_module_for_id(id)
        if table_row.module_name.literal != row["name"]:
            return False
        if table_row.path != row["path"]:
            return False
        return True



class FilesTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, row):
        return self.table.is_file_defined(row["module_id"], row["name"])

    def contents_match(self, row):
        name_included = row["name"] in self.table.get_module_file_names(row["module_id"])
        module_included = row["module_id"] in self.table.get_module_ids_by_file_name(row["name"])
        return name_included and module_included

class TypenamesTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, row):
        return self.table.is_name_defined_in_table(row["name"], row["module_id"])

    def contents_match(self, row):
        type_matches = row["type"] == self.table.get_category_by_name_and_module_id(row["name"], row["module_id"])
        category_has_name = row["name"] in [tok.literal for tok in self.table.get_names_by_category(row["type"])]
        module_has_name = row["name"] in [tok.literal for tok in self.table.get_names_by_module_id(row["module_id"])]
        return type_matches and category_has_name and module_has_name