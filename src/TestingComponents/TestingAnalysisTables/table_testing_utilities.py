import json
from Tokenization.tokenizer import Tokenizer
from ErrorHandling.error_manager import ErrorManager
import symbols
import random

FAILURE = "TEST CASE FAILURE,"


def table_load_tests(
    component_tests, tracker, current_dir, semantic_test, component_name
):
    print("Testing table loading for " + component_name + "...")
    for test_case in component_tests:
        err_manager = ErrorManager()

        database = None
        for i in range(len(test_case["files"])):
            tok = Tokenizer(err_manager)
            try:
                tok.load_src(test_case["files"][i])
            except:
                tok.load_src(current_dir + "/" + test_case["files"][i])
            database = semantic_test(tok, err_manager, database)
            tok.close_src()

        if database is None:
            raise Exception(
                "INTERNAL ERROR: Database was not returned by semantic test function"
            )

        # check for errors
        # retrieve needed tables
        # for each check id, and data against test case
        if err_manager.has_errors() and test_case["errors"] is None:
            print(
                "ERROR: tests expected no errors, but parsing generated errors! See error file."
            )
            while err_manager.has_errors():
                err = err_manager.next_error()
                record_component_test(
                    test_case, tracker, "ok", err.message + ": " + err.token.to_string()
                )
        elif not err_manager.has_errors() and test_case["errors"] is not None:
            print(
                "ERROR: tests expected errors, but parsing generated no errors! See error file."
            )
            record_component_test(test_case, tracker, "error", "ok")
        else:
            run_table_comparisons(database, test_case, tracker)


def get_msg(expect: str, actual: str) -> str:
    return ' expected: "' + str(expect) + '", got "' + str(actual) + '"'


def record_component_test(test_case: dict, tracker, expected: str, result: str) -> None:
    if str(result) != str(expected):
        files = "\n".join([file for file in test_case["files"]])
        msg = FAILURE + "In \n" + files + ":\n" + get_msg(expected, result)
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
    record_component_test(
        test_case,
        tracker,
        "number of objects: " + str(number_of_objects),
        "number of objects: " + str(expected_number_of_objects),
    )


def involved_table_check(database, test_case, tracker):
    expected_tables = list(test_case["tables"].keys())
    for table in database.tables:
        if table in expected_tables:
            record_component_test(
                test_case,
                tracker,
                f"True: {table}",
                f"{str(database.get_table(table).has_contents())}: {table}",
            )
        else:
            record_component_test(
                test_case,
                tracker,
                f"False: {table}",
                f"{str(database.get_table(table).has_contents())}: {table}",
            )


def check_table_contents(database, test_case, tracker):
    expected_tables = list(test_case["tables"].keys())

    for table_name in expected_tables:
        table = database.get_table(table_name)
        object_count = test_case["object_count"]
        test_table = test_case["tables"][table_name]
        query_runner = table_tester_factory(table_name)
        query_runner.set_table(table)
        for row in test_table:
            record_component_test(
                test_case,
                tracker,
                "row is defined in " + table_name,
                "row is defined in " + table_name
                if query_runner.row_is_defined(row)
                else "row is not defined in " + table_name,
            )
            record_component_test(
                test_case,
                tracker,
                "contents match in " + table_name,
                "contents match in " + table_name
                if query_runner.contents_match(row)
                else "contents do not match in " + table_name,
            )
        record_component_test(
            test_case,
            tracker,
            f"{table_name} size:{len(test_table)}",
            f"{table_name} size:{query_runner.table_size()}",
        )
    record_component_test(
        test_case,
        tracker,
        f"object table size:{object_count}",
        f"object table size:{database.object_count()}",
    )


def table_tester_factory(table_name):
    tester = None
    match table_name:
        case "modules":
            tester = ModuleTableTestQueryRunner()
        case "files":
            tester = FilesTableTestQueryRunner()
        case "typenames":
            tester = TypenamesTableTestQueryRunner()
        case "enumerables":
            tester = EnumTableTestQueryRunner()
        case "modifiers":
            tester = ModifierTableTestQueryRunner()
        case "imports":
            tester = ImportTableTestQueryRunner()
        case "defines":
            tester = DefineTableTestQueryRunner()
        case "functions":
            tester = FunctionTableTestQueryRunner()
        case "fn_headers":
            tester = FunctionHeaderTableTestQueryRunner()
        case "interfaces":
            tester = InterfaceTableTestQueryRunner()
        case "unittests":
            tester = UnittestTableTestQueryRunner()
        case "statements":
            tester = StatementTableTestQueryRunner()
        case "structs":
            tester = StructTableTestQueryRunner()
        case _:
            raise Exception(
                f"INTERNAL ERROR: table tester for table {table_name} not found"
            )
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

    def table_size(self):
        return self.table.get_size()


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
        name_included = row["name"] in self.table.get_module_file_names(
            row["module_id"]
        )
        module_included = row["module_id"] in self.table.get_module_ids_by_file_name(
            row["name"]
        )
        return name_included and module_included


class TypenamesTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, row):
        return self.table.is_name_defined_in_table(row["name"], row["type"])

    def contents_match(self, row):
        type_matches = row["type"] in self.table.get_categories_by_name_and_module_id(
            row["name"], row["module_id"]
        )
        category_has_name = row["name"] in [
            tok.literal for tok in self.table.get_names_by_category(row["type"])
        ]
        module_has_name = row["name"] in [
            row.name_token.literal
            for row in self.table.get_items_by_module_id(row["module_id"])
        ]
        return type_matches and category_has_name and module_has_name


class EnumTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, row):
        return self.table.is_object_defined(row["object_id"])

    def contents_match(self, row):
        general_type_token = self.table.get_general_type_token_by_id(row["object_id"])
        type_matches = False
        if general_type_token is not None:
            if row["general_type"] is None:
                raise Exception(
                    "INTERNAL ERROR: Expecting no general type for enumerable type, but one is present"
                )
            type_matches = general_type_token.literal == row["general_type"]
        else:
            type_matches = True
        items = self.table.get_items_by_id(row["object_id"])
        items_match = False
        for item in items:
            for test_item in row["items"]:
                if item.item_name_token.literal == test_item["name"]:
                    if test_item["type"] != None and item.get_value() != None:
                        items_match = test_item["type"] == item.get_value().literal
                    elif test_item["type"] != None and item.get_value() == None:
                        raise Exception(
                            "INTERNAL ERROR: table shows no type, but type expected"
                        )
                    elif test_item["type"] == None and item.get_value() == None:
                        items_match = True
        length_matches = len(items) == len(row["items"])
        return type_matches and items_match and length_matches


class ModifierTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, row):
        return self.table.is_object_defined(row["object_id"])

    def contents_match(self, row):
        if not self.table.is_object_defined(row["object_id"]):
            if len(row["modifier_list"]) == 0:
                return True
        modifier_list = self.table.get_modifier_list_by_id(row["object_id"])
        if len(row["modifier_list"]) != len(modifier_list):
            return False
        elif len(row["modifier_list"]) == 0:
            # means there are no modifiers, so they match
            return True
        for i in range(len(modifier_list)):
            mod = modifier_list[i]
            if mod is None:
                if row["modifier_list"][i] == None:
                    continue
                else:
                    raise Exception(
                        "INTERNAL ERROR: modifier found to be None, but was expected not to be"
                    )
            if mod.literal != row["modifier_list"][i]:
                print("FALSE!_______")
                return False
        return True


class ImportTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, row):
        return self.table.is_object_defined(row["object_id"])

    def contents_match(self, row):
        path = row["path"]
        items = row["items"]
        item_list = self.table.get_items_by_id(row["object_id"])
        path_list = self.table.get_path_by_id(row["object_id"])
        for i in range(len(item_list)):
            if item_list[i].name_token.literal != items[i]["name"]:
                return False
            new_name = item_list[i].new_name_token
            if new_name is not None and items[i]["newname"] is not None:
                if new_name.literal != items[i]["newname"]:
                    return False
            elif new_name is None and items[i]["newname"] is not None:
                raise Exception("INTERNAL ERROR: new name for import is null")
            elif new_name is not None and items[i]["newname"] is None:
                raise Exception("INTERNAL ERROR: test new name is null")

        for i in range(len(path_list)):
            if path_list[i].node_token.literal != path[i]["node"]:
                return False
            direction = path_list[i].direction_token
            if direction is not None and path[i]["direction"] is not None:
                if direction.literal != path[i]["direction"]:
                    return False
            elif direction is None and path[i]["direction"] is not None:
                raise Exception("INTERNAL ERROR: direction for import is null")
            elif direction is not None and path[i]["direction"] is None:
                raise Exception("INTERNAL ERROR: test direction is null")

        return True


class DefineTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, row):
        return self.table.is_object_defined(row["object_id"])

    def contents_match(self, test_row):
        table_row = self.table.get_item_by_id(test_row["object_id"])
        match_list = []
        match_list.append(
            self.match_arg(table_row.built_in_type_token, test_row["built_in_type"])
        )
        match_list.append(
            self.match_arg(table_row.new_type_name_token, test_row["defined_type"])
        )
        match_list.append(self.match_arg(table_row.key_type, test_row["key_type"]))
        match_list.append(self.match_arg(table_row.value_type, test_row["value_type"]))
        match_list.append(
            self.match_args(table_row.arg_list, test_row["arg_type_list"])
        )
        match_list.append(self.match_arg(table_row.result_type, test_row["union_type"]))
        for match in match_list:
            if not match:
                return False
        return True

    def match_args(self, table_row_arg_list, test_row_arg_list):
        if table_row_arg_list is None:
            if test_row_arg_list is None:
                return True
            return False
        elif test_row_arg_list is None:
            raise Exception(
                "INTERNAL ERROR: test case has argument list for function, table does not"
            )
        if len(table_row_arg_list) != len(test_row_arg_list):
            return False
        for arg in table_row_arg_list:
            if arg.literal not in test_row_arg_list:
                return False
        return True

    def match_arg(self, lhs, rhs):
        if lhs is None:
            if rhs is None:
                return True
            return False
        return lhs.literal == rhs


class InterfaceTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, test_row):
        return self.table.is_object_defined(test_row["object_id"])

    def contents_match(self, test_row):
        table_row = self.table.get_item_by_id(test_row["object_id"])
        other_rows = self.table.get_rows_by_module_id(test_row["module_id"])
        if len(table_row.fn_header_ids) != len(test_row["header_ids"]):
            return False
        for id in table_row.fn_header_ids:
            if id not in test_row["header_ids"]:
                return False
        for other_row in other_rows:
            if other_row.object_id == test_row["object_id"]:
                return True
        return False


class FunctionTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, test_row):
        return self.table.is_object_defined(test_row["object_id"])

    def contents_match(self, test_row):
        function_row = self.table.get_item_by_id(test_row["object_id"])
        return function_row.header_id == test_row["header_id"]


class FunctionHeaderTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, test_row):
        return self.table.is_object_defined(test_row["object_id"])

    def contents_match(self, test_row):
        table_row = self.table.get_item_by_id(test_row["object_id"])
        if table_row.return_type_token and not test_row["return_type"]:
            return False
        if not table_row.return_type_token and test_row["return_type"]:
            return False
        if test_row["return_type"] != table_row.return_type_token.literal:
            return False

        if test_row["args"] and not table_row.arguments:
            raise Exception("INTERNAL ERROR: test row has args, but table row does not")
        if table_row.arguments and not test_row["args"]:
            raise Exception("INTERNAL ERROR: table has args, but test row does not")
        if len(test_row["args"]) != len(table_row.arguments):
            return False
        for i in range(len(test_row["args"])):
            test_arg = test_row["args"][i]
            header_arg = table_row.arguments[i]
            if test_arg["name"] != header_arg.arg_name_token.literal:
                return False
            if test_arg["type"] != header_arg.arg_type_token.literal:
                return False
            if test_arg["default_value"] and not header_arg.default_value_token:
                raise Exception(
                    "INTERNAL ERROR: test row has default value, but table row does not"
                )
            if not test_arg["default_value"] and header_arg.default_value_token:
                raise Exception(
                    "INTERNAL ERROR: test row has no default value, but table row does"
                )
            if not test_arg["default_value"] and not header_arg.default_value_token:
                continue
            if test_arg["default_value"] != header_arg.default_value_token.literal:
                return False
        return True

class UnittestTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, test_row):
        return self.table.is_object_defined(test_row["object_id"])

    def contents_match(self, test_row):
        table_row = self.table.get_item_by_id(test_row["object_id"])
        if test_row["name"] != table_row.name.literal:
            return False
        if test_row["module_id"] != table_row.module_id:
            return False
        return True
    
    def table_size(self):
        return self.table.get_size()

class StatementTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, test_row):
        return self.table.is_object_defined(
            test_row["container_object_id"], test_row["sequence_num"]
        )

    def contents_match(self, test_row):
        table_row = self.table.get_item_by_id_and_seq_num(
            test_row["container_object_id"], test_row["sequence_num"]
        )
        if test_row["container_object_id"] != table_row.container_object_id:
            raise Exception(
                "INTERNAL ERROR: container object id used to retrieve object, but wrong one returned"
            )
        if test_row["sequence_num"] != table_row.sequence_num:
            raise Exception(
                "INTERNAL ERROR: sequence number used to retrieve object, but wrong one returned"
            )
        if test_row["scope_depth"] != table_row.scope_depth:
            return False
        if test_row["stmt_type"] != table_row.stmt_type_token.type_symbol:
            return False
        if test_row["stmt_specific_items"] is None:
            return True

        return False


class StructTableTestQueryRunner(TestQueryRunner):
    def __init__(self) -> None:
        pass

    def row_is_defined(self, test_row):
        return self.table.is_object_defined(test_row["object_id"])

    def contents_match(self, test_row):
        table_row = self.table.get_item_by_id(test_row["object_id"])
        table_fn_ids = table_row.function_ids
        test_row_fn_ids = test_row["function_ids"]
        if not self.check_fn_ids(table_fn_ids, test_row_fn_ids):
            return False
        table_fields = table_row.fields
        test_row_fields = test_row["fields"]
        if not self.check_fields(table_fields, test_row_fields):
            return False
        interfaces = table_row.interfaces
        test_interfaces = test_row["interfaces"]
        if not self.check_interfaces(interfaces, test_interfaces):
            return False
        return True

    def check_fn_ids(self, table_fn_ids, test_row_fn_ids):
        if len(table_fn_ids) != len(test_row_fn_ids):
            return False
        for id in table_fn_ids:
            if id not in test_row_fn_ids:
                return False
        return True

    def check_fields(self, table_fields, test_row_fields):
        if len(table_fields) != len(test_row_fields):
            return False
        for i in range(len(table_fields)):
            field = table_fields[i]
            test_field = test_row_fields[i]
            if field.public_token and test_field["mod"]:
                if field.public_token.literal != test_field["mod"]:
                    return False
            else:
                raise Exception(
                    "INTERNAL ERROR: either test or table field missing modifier"
                )

            if field.field_name_token.literal != test_field["name"]:
                return False

            if field.type_token.literal != test_field["type"]:
                return False

        return True

    def check_interfaces(self, interfaces, test_interfaces):
        if len(interfaces) != len(test_interfaces):
            return False

        for i in range(len(interfaces)):
            if interfaces[i].literal != test_interfaces[i]:
                return False
        return True
