from TestingComponents.testing_utilities import get_json_from_file, call_parsing_tests, call_tokenizer_tests, parser_happy_path_tests
from TestingComponents.testing_parsing_driver import TestingParsingDriver

from Parsing.expression_parsing import parse_expression
from Parsing.ExternalStatementParsing.enum_parsing import parse_enum
from Parsing.ExternalStatementParsing.union_parsing import parse_union
from Parsing.ExternalStatementParsing.error_parsing import parse_error
from Parsing.ExternalStatementParsing.import_parsing import parse_import 
from Parsing.ExternalStatementParsing.module_parsing import parse_module 
from Parsing.ExternalStatementParsing.define_parsing import parse_define
from Parsing.ExternalStatementParsing.interface_parsing import parse_interface
from Parsing.ExternalStatementParsing.function_parsing import parse_function
from Parsing.ExternalStatementParsing.unittest_parsing import parse_unittest
from Parsing.ExternalStatementParsing.struct_parsing import parse_struct
from Parsing.InternalStatementParsing.assignment_parsing import parse_assignment
from Parsing.InternalStatementParsing.re_assignment_or_call_parsing import parse_re_assignment_or_call, parse_defer
from Parsing.InternalStatementParsing.if_parsing import parse_if
from Parsing.InternalStatementParsing.elif_parsing import parse_elif
from Parsing.InternalStatementParsing.else_parsing import parse_else
from Parsing.InternalStatementParsing.unless_parsing import parse_unless
from Parsing.InternalStatementParsing.loop_parsing import parse_loop
from Parsing.InternalStatementParsing.while_parsing import parse_while
from Parsing.InternalStatementParsing.return_parsing import parse_return
from Parsing.InternalStatementParsing.break_parsing import parse_break
from Parsing.InternalStatementParsing.continue_parsing import parse_continue
from Parsing.InternalStatementParsing.switch_parsing import parse_switch
from Parsing.InternalStatementParsing.for_parsing import parse_for
from Parsing.InternalStatementParsing.statement_parsing import parse_statements
from Parsing.parse import parse_src

def tokenizer_parser_tests(tracker, current_dir: str) -> None:
    for test in TEST_JSON:
        component_tests = get_json_from_file(current_dir + "/" + test["test_manifest_file"])
        general_component = test['general_component']
        print(general_component)
        test_fn = None
        if general_component == "scanner":
            call_tokenizer_tests(component_tests, tracker, current_dir)
            continue
        if general_component == "expparser":
            test_fn = parse_expression_test
        elif general_component == "enumparser":
            test_fn = enum_parse_test
        elif general_component == "unionparser":
            test_fn = union_parse_test
        elif general_component == "errorparser":
            test_fn = error_parse_test
        elif general_component == "importparser":
            test_fn = import_parse_test
        elif general_component == "moduleparser":
            test_fn = module_parse_test
        elif general_component == "defineparser":
            test_fn = define_parse_test
        elif general_component == "interfaceparser":
            test_fn = interface_parse_test
        elif general_component == "functionparser":
            test_fn = function_parse_test
        elif general_component == "unittestparser":
            test_fn = unittest_parse_test
        elif general_component == "structparser":
            test_fn = struct_parse_test
        elif general_component == "assignparser":
            test_fn = assign_parse_test
        elif general_component == "reassignorcallparser":
            test_fn = reassign_parse_test
        elif general_component == "deferparser":
            test_fn = defer_parse_test
        elif general_component == "ifparser":
            test_fn = if_parse_test
        elif general_component == "elifparser":
            test_fn = elif_parse_test
        elif general_component == "elseparser":
            test_fn = else_parse_test
        elif general_component == "unlessparser":
            test_fn = unless_parse_test
        elif general_component == "loopparser":
            test_fn = loop_parse_test
        elif general_component == "whileparser":
            test_fn = while_parse_test
        elif general_component == "returnparser":
            test_fn = return_parse_test
        elif general_component == "breakparser":
            test_fn = break_parse_test
        elif general_component == "continueparser":
            test_fn = continue_parse_test
        elif general_component == "switchparser":
            test_fn = switch_parse_test
        elif general_component == "forparser":
            test_fn = for_parse_test
        elif general_component == "statementsequences":
            test_fn = statement_parse_test
        elif general_component == "statementcombinations":
            test_fn = statement_parse_test
        elif general_component == "mainparserJSON":
            test_fn = main_parse_test
        elif general_component == "mainparserJSONpt2":
            test_fn = main_parse_test
        elif general_component == "happy_path":
            test_fn = happy_path
            parser_happy_path_tests(component_tests, tracker, test_fn, current_dir)
            continue
        else:
            continue
        if test_fn is None:
            raise Exception("INTERNAL ERROR: parsing test function not found")
        call_parsing_tests(component_tests, tracker, current_dir, test_fn, general_component)
    print("\nDone phase one tests\n")


def parse_expression_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_expression(driver)


def enum_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_enum(driver)


def union_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_union(driver)


def error_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_error(driver)


def import_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_import(driver)


def module_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_module(driver)


def define_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_define(driver)


def interface_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_interface(driver)


def function_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager, True)
    return parse_function(driver)


def unittest_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager, True)
    return parse_unittest(driver)


def struct_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_struct(driver)


def assign_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_assignment(driver)


def reassign_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_re_assignment_or_call(driver)


def defer_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_defer(driver)


def if_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager, True)
    return parse_if(driver)


def elif_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager, True)
    return parse_elif(driver)


def else_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_else(driver)


def unless_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager, True)
    return parse_unless(driver)


def loop_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_loop(driver)


def while_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_while(driver)


def return_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_return(driver)


def break_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_break(driver)


def continue_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_continue(driver)


def switch_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_switch(driver)


def for_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager, True)
    return parse_for(driver)


def statement_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_statements(driver)


def main_parse_test(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_src(driver)

def happy_path(tok, err_manager):
    driver = TestingParsingDriver(tok, err_manager)
    return parse_src(driver)


TEST_JSON = [
    {
        "general_component" : "scanner",
        "test_manifest_file" : "../TestFiles/ScannerTests/scanner_manualtests.json"
    },
    {
        "general_component" : "scanner",
        "test_manifest_file" : "../TestFiles/ScannerTests/scanner_auto_made_tests.json"
    },
    {
        "general_component" : "expparser",
        "test_manifest_file" : "../TestFiles/ParserTests/expparser_error_tests.json"
    },
    {
        "general_component" : "expparser",
        "test_manifest_file" : "../TestFiles/ParserTests/expparser_error_tests_pt_2.json"
    },
    {
        "general_component" : "expparser",
        "test_manifest_file" : "../TestFiles/ParserTests/expparser_manual_tests.json"
    },
    {
        "general_component" : "expparser",
        "test_manifest_file" : "../TestFiles/ParserTests/expparser_auto_tests.json"
    },
    {
        "general_component" : "moduleparser",
        "test_manifest_file" : "../TestFiles/ParserTests/modparser_manual_tests.json"
    },
    {
        "general_component" : "importparser",
        "test_manifest_file" : "../TestFiles/ParserTests/importparser_manual_tests.json"
    },
    {
        "general_component" : "defineparser",
        "test_manifest_file" : "../TestFiles/ParserTests/defineparser_manual_tests.json"
    },
    {
        "general_component" : "enumparser",
        "test_manifest_file" : "../TestFiles/ParserTests/enumparser_manual_tests.json"
    },
    {
        "general_component" : "errorparser",
        "test_manifest_file" : "../TestFiles/ParserTests/errorparser_manual_tests.json"
    },
    {
        "general_component" : "unionparser",
        "test_manifest_file" : "../TestFiles/ParserTests/unionparser_manual_tests.json"
    },
    {
        "general_component" : "unittestparser",
        "test_manifest_file" : "../TestFiles/ParserTests/unittestparser_manual_tests.json"
    },
    {
        "general_component" : "functionparser",
        "test_manifest_file" : "../TestFiles/ParserTests/functionparser_manual_tests.json"
    },
    {
        "general_component" : "interfaceparser",
        "test_manifest_file" : "../TestFiles/ParserTests/interfaceparser_manual_tests.json"
    },
    {
        "general_component" : "structparser",
        "test_manifest_file" : "../TestFiles/ParserTests/structparser_manual_tests.json"
    },
    {
        "general_component" : "returnparser",
        "test_manifest_file" : "../TestFiles/ParserTests/returnparser_manual_tests.json"
    },
    {
        "general_component" : "continueparser",
        "test_manifest_file" : "../TestFiles/ParserTests/continueparser_manual_tests.json"
    },
    {
        "general_component" : "breakparser",
        "test_manifest_file" : "../TestFiles/ParserTests/breakparser_manual_tests.json"
    },
    {
        "general_component" : "loopparser",
        "test_manifest_file" : "../TestFiles/ParserTests/loopparser_manual_tests.json"
    },
    {
        "general_component" : "switchparser",
        "test_manifest_file" : "../TestFiles/ParserTests/switchparser_manual_tests.json"
    },
    {
        "general_component" : "ifparser",
        "test_manifest_file" : "../TestFiles/ParserTests/ifparser_manual_tests.json"
    },
    {
        "general_component" : "elseparser",
        "test_manifest_file" : "../TestFiles/ParserTests/elseparser_manual_tests.json"
    },
    {
        "general_component" : "unlessparser",
        "test_manifest_file" : "../TestFiles/ParserTests/unlessparser_manual_tests.json"
    },
    {
        "general_component" : "elifparser",
        "test_manifest_file" : "../TestFiles/ParserTests/elifparser_manual_tests.json"
    },
    {
        "general_component" : "assignparser",
        "test_manifest_file" : "../TestFiles/ParserTests/assignparser_manual_tests.json"
    },
    {
        "general_component" : "whileparser",
        "test_manifest_file" : "../TestFiles/ParserTests/whileparser_manual_tests.json"
    },
    {
        "general_component" : "forparser",
        "test_manifest_file" : "../TestFiles/ParserTests/forparser_manual_tests.json"
    },
    {
        "general_component" : "reassignorcallparser",
        "test_manifest_file" : "../TestFiles/ParserTests/reassignorcallparser_manual_tests.json"
    },
    {
        "general_component" : "statementparserwdummy",
        "test_manifest_file" : "../TestFiles/ParserTests/statement_with_dummy_parser_manual_tests.json"
    },
    {
        "general_component" : "statementsequences",
        "test_manifest_file" : "../TestFiles/ParserTests/statement_sequence_tests.json"
    },
    {
        "general_component" : "mainparser",
        "test_manifest_file" : "../TestFiles/ParserTests/main_parser_statement_tests.json"
    },
    {
        "general_component" : "mainparserJSON",
        "test_manifest_file" : "../TestFiles/ParserTests/main_parser_json_tests.json"
    },
    {
        "general_component" : "mainparserJSONpt2",
        "test_manifest_file" : "../TestFiles/ParserTests/main_parser_json_tests_part_two.json"
    },
    {
        "general_component": "happy_path",
        "test_manifest_file": "../TestFiles/SemanticAnalyzerTests/function_return_paths_generated_tests.json"
    }
] 