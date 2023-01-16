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
from Parsing.InternalStatementParsing.re_assignment_parsing import parse_re_assignment, parse_defer
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

def phase_one_tests(tracker, test_json, current_dir: str) -> None:
    for test in test_json:
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
    return parse_re_assignment(driver)


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
