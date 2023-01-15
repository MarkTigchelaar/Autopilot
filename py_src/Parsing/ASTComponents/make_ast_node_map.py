from Parsing.ASTComponents.ExternalComponents.enum_statement import EnumStatement
from Parsing.ASTComponents.ExternalComponents.union_statement import UnionStatement
from Parsing.ASTComponents.ExternalComponents.error_statement import ErrorStatement
from Parsing.ASTComponents.ExternalComponents.import_statement import ImportStatement
from Parsing.ASTComponents.ExternalComponents.module_statement import ModuleStatement
from Parsing.ASTComponents.ExternalComponents.define_statement import \
DefineStatement, KeyValueType, LinearType, FailableType, FunctionType
from Parsing.ASTComponents.ExternalComponents.interface_statement import InterfaceStatement
from Parsing.ASTComponents.ExternalComponents.function_header_statement import FunctionHeaderStatement, FunctionArgument
from Parsing.ASTComponents.ExternalComponents.function_statement import FunctionStatement
from Parsing.ASTComponents.ExternalComponents.unittest_statement import UnittestStatement
from Parsing.ASTComponents.ExternalComponents.struct_statement import StructStatement, StructField
from Parsing.ASTComponents.InternalComponents.assign_statement import AssignmentStatement
from Parsing.ASTComponents.InternalComponents.assign_statement import AssignmentStatement
from Parsing.ASTComponents.InternalComponents.re_assign_or_method_call import ReassignmentOrMethodCall 
from Parsing.ASTComponents.InternalComponents.defer_statement import DeferStatement
from Parsing.ASTComponents.InternalComponents.if_statement import IfStatement
from Parsing.ASTComponents.InternalComponents.elif_statement import ElifStatement
from Parsing.ASTComponents.InternalComponents.else_statement import ElseStatement
from Parsing.ASTComponents.InternalComponents.unless_statement import UnlessStatement
from Parsing.ASTComponents.InternalComponents.loop_statement import LoopStatement
from Parsing.ASTComponents.InternalComponents.while_statement import WhileStatement
from Parsing.ASTComponents.InternalComponents.return_statement import ReturnStatement
from Parsing.ASTComponents.InternalComponents.break_statement import BreakStatement
from Parsing.ASTComponents.InternalComponents.continue_statement import ContinueStatement
from Parsing.ASTComponents.InternalComponents.switch_statement import SwitchStatement, CaseStatement
from Parsing.ASTComponents.InternalComponents.for_statement import ForStatement
from Parsing.ASTComponents.ExpressionComponents.name_expression import NameExpression
from Parsing.ASTComponents.ExpressionComponents.prefix_expression import PrefixExpression
from Parsing.ASTComponents.ExpressionComponents.collection_expression import CollectionExpression
from Parsing.ASTComponents.ExpressionComponents.operator_expression import OperatorExpression
from Parsing.ASTComponents.ExpressionComponents.function_call_expression import FunctionCallExpression
from Parsing.ASTComponents.ExpressionComponents.method_call_or_field_expression import MethodCallOrFieldExpression
from Parsing.ASTComponents.ExpressionComponents.collection_access_expression import CollectionAccessExpression
from Parsing.ASTComponents import ast_node_keys


def make_ast_map():
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
    return EnumStatement()

def make_union_statement():
    return UnionStatement()

def make_error_statement():
    return ErrorStatement()

def make_import_statement():
    return ImportStatement()

def make_module_statement():
    return ModuleStatement()

def make_define_statement():
    return DefineStatement()

def make_key_value_type_definiton():
    return KeyValueType()

def make_linear_type_definition():
    return LinearType()

def make_failable_type_definition():
    return FailableType()

def make_function_type_definition():
    return FunctionType()

def make_interface_statement():
    return InterfaceStatement()

def make_function_argument():
    return FunctionArgument()

def make_function_statement():
    return FunctionStatement()

def make_unittest_statement():
    return UnittestStatement()

def make_struct_statement():
    return StructStatement()

def make_struct_field():
    return StructField()

def make_function_header_statement():
    return FunctionHeaderStatement()

def make_assignment_statement():
    return AssignmentStatement()

def make_defer_statement():
    return DeferStatement()

def make_re_assignment_statement():
    return ReassignmentOrMethodCall()

def make_if_statement():
    return IfStatement()

def make_elif_statement():
    return ElifStatement()

def make_else_statement():
    return ElseStatement()

def make_unless_statement():
    return UnlessStatement()

def make_loop_statement():
    return LoopStatement()

def make_while_statement():
    return WhileStatement()

def make_return_statement():
    return ReturnStatement()

def make_break_statement():
    return BreakStatement()

def make_continue_statement():
    return ContinueStatement()

def make_switch_statement():
    return SwitchStatement()

def make_case_statement():
    return CaseStatement()

def make_for_statement():
    return ForStatement()

def make_name_expression_node():
    return NameExpression()

def make_prefix_expression_node():
    return PrefixExpression()

def make_collection_expression():
    return CollectionExpression()

def make_operator_expresison():
    return OperatorExpression()

def make_function_call_expression():
    return FunctionCallExpression()

def make_collection_access_expression():
    return CollectionAccessExpression()

def make_method_or_field_expression():
    return MethodCallOrFieldExpression()
