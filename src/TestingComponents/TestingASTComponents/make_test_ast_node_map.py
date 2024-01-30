from TestingComponents.TestingASTComponents.TestingExternalComponents.testing_enum_statement import TestingEnumStatement
from TestingComponents.TestingASTComponents.TestingExternalComponents.testing_union_statement import TestingUnionStatement
from TestingComponents.TestingASTComponents.TestingExternalComponents.testing_error_statement import TestingErrorStatement
from TestingComponents.TestingASTComponents.TestingExternalComponents.testing_import_statement import TestingImportStatement
from TestingComponents.TestingASTComponents.TestingExternalComponents.testing_module_statement import TestingModuleStatement
from TestingComponents.TestingASTComponents.TestingExternalComponents.testing_define_statement import \
TestingDefineStatement, TestingKeyValueType, TestingLinearType, TestingFailableType, TestingFunctionType
from TestingComponents.TestingASTComponents.TestingExternalComponents.testing_interface_statement import TestingInterfaceStatement
from TestingComponents.TestingASTComponents.TestingExternalComponents.testing_function_header_statement import TestingFunctionHeader, TestingFunctionArgument
from TestingComponents.TestingASTComponents.TestingExternalComponents.testing_function_statement import TestingFunctionStatement
from TestingComponents.TestingASTComponents.TestingExternalComponents.testing_unittest_statement import TestingUnittestStatement
from TestingComponents.TestingASTComponents.TestingExternalComponents.testing_struct_statement import TestingStructStatement, TestingStructField
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_assign_statement import TestingAssignmentStatement
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_assign_statement import TestingAssignmentStatement
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_re_assign_or_method_call_statement import TestingReAssignOrMethodCallStatement 
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_defer_statement import TestingDeferStatement
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_if_statement import TestingIfStatement
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_elif_statement import TestingElifStatement
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_else_statement import TestingElseStatement
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_unless_statement import TestingUnlessStatement
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_loop_statement import TestingLoopStatement
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_while_statement import TestingWhileStatement
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_return_statement import TestingReturnStatement
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_break_statement import TestingBreakStatement
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_continue_statement import TestingContinueStatement
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_switch_statement import TestingSwitchStatement, TestingCaseStatement
from TestingComponents.TestingASTComponents.TestingInternalComponents.testing_for_statement import TestingForStatement
from TestingComponents.TestingASTComponents.TestingExpressionComponents.testing_name_expression import TestingNameExpression
from TestingComponents.TestingASTComponents.TestingExpressionComponents.testing_prefix_expression import TestingPrefixExpression
from TestingComponents.TestingASTComponents.TestingExpressionComponents.testing_collection_expression import TestingCollectionExpression
from TestingComponents.TestingASTComponents.TestingExpressionComponents.testing_operator_expression import TestingOperatorExpression
from TestingComponents.TestingASTComponents.TestingExpressionComponents.testing_function_call_expression import TestingFunctionCallExpression
from TestingComponents.TestingASTComponents.TestingExpressionComponents.testing_method_call_or_field_expression import TestingMethodCallOrFieldExpression
from TestingComponents.TestingASTComponents.TestingExpressionComponents.testing_collection_access_expression import TestingCollectionAccessExpression
from ASTComponents import ast_node_keys


def make_test_ast_map():
    test_ast_node_map = dict()
    test_ast_node_map[ast_node_keys.ENUM] = make_enum_statement
    test_ast_node_map[ast_node_keys.UNION] = make_union_statement
    test_ast_node_map[ast_node_keys.ERROR] = make_error_statement
    test_ast_node_map[ast_node_keys.IMPORT] = make_import_statement
    test_ast_node_map[ast_node_keys.MODULE] = make_module_statement
    test_ast_node_map[ast_node_keys.DEFINE] = make_define_statement
    test_ast_node_map[ast_node_keys.KV_DEFINE] = make_key_value_type_definiton
    test_ast_node_map[ast_node_keys.LINEAR_DEFINE] = make_linear_type_definition
    test_ast_node_map[ast_node_keys.FAIL_DEFINE] = make_failable_type_definition
    test_ast_node_map[ast_node_keys.FN_SIG_DEFINE] = make_function_type_definition
    test_ast_node_map[ast_node_keys.FN_ARG_DEFINE] = make_function_argument
    test_ast_node_map[ast_node_keys.INTERFACE_DEFINE] = make_interface_statement
    test_ast_node_map[ast_node_keys.FN_STMT] = make_function_statement
    test_ast_node_map[ast_node_keys.FN_HEADER] = make_function_header_statement
    test_ast_node_map[ast_node_keys.UNITTEST_STMT] = make_unittest_statement
    test_ast_node_map[ast_node_keys.STRUCT_STMT] = make_struct_statement
    test_ast_node_map[ast_node_keys.STRUCT_FIELD_STMT] = make_struct_field
    test_ast_node_map[ast_node_keys.ASSIGN_EXP] = make_assignment_statement
    test_ast_node_map[ast_node_keys.DEFER_STMT] = make_defer_statement
    test_ast_node_map[ast_node_keys.REASSIGN_STMT] = make_re_assignment_statement
    test_ast_node_map[ast_node_keys.IF_STMT] = make_if_statement
    test_ast_node_map[ast_node_keys.ELIF_STMT] = make_elif_statement
    test_ast_node_map[ast_node_keys.ELSE_STMT] = make_else_statement
    test_ast_node_map[ast_node_keys.UNLESS_STMT] = make_unless_statement
    test_ast_node_map[ast_node_keys.LOOP_STMT] = make_loop_statement
    test_ast_node_map[ast_node_keys.WHILE_STMT] = make_while_statement
    test_ast_node_map[ast_node_keys.RETURN_STMT] = make_return_statement
    test_ast_node_map[ast_node_keys.BREAK_STMT] = make_break_statement
    test_ast_node_map[ast_node_keys.CONT_STMT] = make_continue_statement
    test_ast_node_map[ast_node_keys.SWITCH_STMT] = make_switch_statement
    test_ast_node_map[ast_node_keys.CASE_STMT] = make_case_statement
    test_ast_node_map[ast_node_keys.FOR_STMT] = make_for_statement
    test_ast_node_map[ast_node_keys.NAME_EXP] = make_name_expression_node
    test_ast_node_map[ast_node_keys.PREFIX_EXP] = make_prefix_expression_node
    test_ast_node_map[ast_node_keys.COLLECT_EXP] = make_collection_expression
    test_ast_node_map[ast_node_keys.OP_EXP] = make_operator_expresison
    test_ast_node_map[ast_node_keys.FN_CALL_EXP] = make_function_call_expression
    test_ast_node_map[ast_node_keys.COLLECT_ACCESS_EXP] = make_collection_access_expression
    test_ast_node_map[ast_node_keys.METHOD_OR_FIELD_EXP] = make_method_or_field_expression
    return test_ast_node_map

def make_enum_statement():
    return TestingEnumStatement()

def make_union_statement():
    return TestingUnionStatement()

def make_error_statement():
    return TestingErrorStatement()

def make_import_statement():
    return TestingImportStatement()

def make_module_statement():
    return TestingModuleStatement()

def make_define_statement():
    return TestingDefineStatement()

def make_key_value_type_definiton():
    return TestingKeyValueType()

def make_linear_type_definition():
    return TestingLinearType()

def make_failable_type_definition():
    return TestingFailableType()

def make_function_type_definition():
    return TestingFunctionType()

def make_interface_statement():
    return TestingInterfaceStatement()

def make_function_argument():
    return TestingFunctionArgument()

def make_function_statement():
    return TestingFunctionStatement()

def make_unittest_statement():
    return TestingUnittestStatement()

def make_struct_statement():
    return TestingStructStatement()

def make_struct_field():
    return TestingStructField()

def make_function_header_statement():
    return TestingFunctionHeader()

def make_assignment_statement():
    return TestingAssignmentStatement()

def make_defer_statement():
    return TestingDeferStatement()

def make_re_assignment_statement():
    return TestingReAssignOrMethodCallStatement()

def make_if_statement():
    return TestingIfStatement()

def make_elif_statement():
    return TestingElifStatement()

def make_else_statement():
    return TestingElseStatement()

def make_unless_statement():
    return TestingUnlessStatement()

def make_loop_statement():
    return TestingLoopStatement()

def make_while_statement():
    return TestingWhileStatement()

def make_return_statement():
    return TestingReturnStatement()

def make_break_statement():
    return TestingBreakStatement()

def make_continue_statement():
    return TestingContinueStatement()

def make_switch_statement():
    return TestingSwitchStatement()

def make_case_statement():
    return TestingCaseStatement()

def make_for_statement():
    return TestingForStatement()

def make_name_expression_node():
    return TestingNameExpression()

def make_prefix_expression_node():
    return TestingPrefixExpression()

def make_collection_expression():
    return TestingCollectionExpression()

def make_operator_expresison():
    return TestingOperatorExpression()

def make_function_call_expression():
    return TestingFunctionCallExpression()

def make_collection_access_expression():
    return TestingCollectionAccessExpression()

def make_method_or_field_expression():
    return TestingMethodCallOrFieldExpression()
