from Testing.progress_tracker import ProgressTracker
from Testing.Parsing.ExpressionParsing.expression_parser_tests import (
    run_expression_parser_tests,
)
from Testing.Parsing.ExternalStatementTests.ModuleStatementParsing.module_statement_parsing_tests import (
    test_module_statement_parser,
)
from Testing.Parsing.ExternalStatementTests.ImportStatementParsing.import_statement_parsing_tests import (
    test_import_statement_parser,
)
from Testing.Parsing.ExternalStatementTests.DefineStatementParsing.define_statement_parsing_tests import (
    test_define_statement_parser,
)
from Testing.Parsing.ExternalStatementTests.EnumStatementParsing.enum_parsing_test import (
    test_enum_statement_parser,
)
from Testing.Parsing.ExternalStatementTests.ErrorStatementParsing.error_parsing_tests import (
    test_error_statement_parser,
)
from Testing.Parsing.ExternalStatementTests.UnionStatementParsing.union_parsing_tests import (
    test_union_statement_parser,
)
from Testing.Parsing.ExternalStatementTests.InterfaceStatementParsing.interface_parsing_tests import (
    test_interface_statement_parser,
)
from Testing.Parsing.ExternalStatementTests.UnittestStatementParsing.unittest_parsing_tests import (
    test_unittest_statement_parser,
)
from Testing.Parsing.ExternalStatementTests.FunctionStatementParsing.function_parsing_tests import (
    test_function_statement_parser,
)
from Testing.Parsing.ExternalStatementTests.StructStatementParsing.struct_parsing_tests import (
    test_struct_statement_parser,
)
from Testing.Parsing.InternalStatementTests.ContinueStatementParsing.continue_parsing_tests import (
    test_continue_parser,
)
from Testing.Parsing.InternalStatementTests.BreakStatementParsing.break_statement_parsing_tests import (
    test_break_parser,
)
from Testing.Parsing.InternalStatementTests.ReturnStatementParsing.return_statement_parsing_tests import (
    test_return_parser,
)
from Testing.Parsing.InternalStatementTests.IfStatementParsing.if_statement_parsing_tests import (
    test_if_statement_parser
)
from Testing.Parsing.InternalStatementTests.ElifStatementParsing.elif_statement_parsing_tests import (
    test_elif_statement_parser
)
from Testing.Parsing.InternalStatementTests.ElseStatementParsing.else_statement_parsing_tests import (
    test_else_statement_parser
)
from Testing.Parsing.InternalStatementTests.UnlessStatementParsing.unless_statement_parsing_tests import (
    test_unless_statement_parser
)
from Testing.Parsing.InternalStatementTests.SwitchStatementParsing.switch_statement_parsing_tests import (
    test_switch_statement_parser
)
from Testing.Parsing.InternalStatementTests.ForStatementParsing.for_statement_parsing_tests import (
    test_for_statement_parser
)
from Testing.Parsing.InternalStatementTests.LoopStatementParsing.loop_statement_parsing_tests import (
    test_loop_statement_parser
)
from Testing.Parsing.InternalStatementTests.ReassignOrCallStatementParsing.reassign_or_call_statement_parsing_tests import (
    test_reassign_statement_parser
)
from Testing.Parsing.InternalStatementTests.AssignStatementParsing.assign_statement_parsing_tests import (
    test_assign_statement_parser
)
from Testing.Parsing.InternalStatementTests.StatementSequenceParsing.statement_sequence_parsing_tests import (
    test_statement_sequence_parser
)
from Testing.Parsing.SourceFileParsing.source_file_parsing_tests import test_source_file_parser

def run_parsing_tests(progress_tracker: ProgressTracker) -> None:
    run_external_statement_parsing_tests(progress_tracker)
    run_expression_parser_tests(progress_tracker)
    run_internal_statement_parsing_tests(progress_tracker)
    test_source_file_parser(progress_tracker)


def run_external_statement_parsing_tests(progress_tracker: ProgressTracker) -> None:

    test_module_statement_parser(progress_tracker)
    test_import_statement_parser(progress_tracker)
    test_define_statement_parser(progress_tracker)
    test_enum_statement_parser(progress_tracker)
    test_error_statement_parser(progress_tracker)
    test_union_statement_parser(progress_tracker)

    test_interface_statement_parser(progress_tracker)
    test_unittest_statement_parser(progress_tracker)
    test_function_statement_parser(progress_tracker)
    test_struct_statement_parser(progress_tracker)




def run_internal_statement_parsing_tests(progress_tracker: ProgressTracker) -> None:
    test_continue_parser(progress_tracker)
    test_break_parser(progress_tracker)
    test_return_parser(progress_tracker)
    test_if_statement_parser(progress_tracker)
    test_elif_statement_parser(progress_tracker)
    test_else_statement_parser(progress_tracker)
    test_unless_statement_parser(progress_tracker)
    test_switch_statement_parser(progress_tracker)
    test_for_statement_parser(progress_tracker)
    test_loop_statement_parser(progress_tracker)
    test_reassign_statement_parser(progress_tracker)
    test_assign_statement_parser(progress_tracker)
    test_statement_sequence_parser(progress_tracker)




# TODO
"""
    Full parser tests (multiple files, same module)
    Module collection tests
    fix up module path finder + tests
    process imports (multiple imports, existance of modules) <- partially semantic analysis,
    but is needed, otherwise compiler cant function
    Check that imports (edges) and modules (nodes) form a DAG
    Make compiler main.py file, with arg parser, ensure everything works up to parsing completion
    Parsing is Done!
"""