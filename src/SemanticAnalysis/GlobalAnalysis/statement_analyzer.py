from keywords import is_primitive_type, is_boolean_literal
from symbols import VAR, BOOL, INT, LONG, FLOAT, DOUBLE
from SemanticAnalysis.GlobalAnalysis.ExpressionAnalyzer.expression_analyzer import (
    ExpressionAnalyzer,
)
import ErrorHandling.semantic_error_messages as ErrMsgs
from SemanticAnalysis.Database.Queries.module_items_query import ModuleItemsQuery
from SemanticAnalysis.Database.Queries.import_items_in_module_query import ImportItemsInModuleQuery


# from SemanticAnalysis.GlobalAnalysis.SpecificStatementAnalyzers.declaration_analyzer import DeclarationAnalyzer
# from SemanticAnalysis.Database.Queries.statement_data_query import StatementDataViewQuery
"""
check declarations of variables:
if type matches, or at least record inferred type
check if some other declaration follows it (shadowing declaration)
check if declared variable is reassigned to / mutated (if let keyword is used, then it is not allowed)

"""


class LocalVariableDeclaration:
    def __init__(self) -> None:
        self.name_token = None
        self.type_token = None
        self.mutability_token = None
        self.sequence_number = None
        self.scope_depth = None
        self.is_loop_variable = False
        # hashability, eq, and ordering info
        self.variable_type_data = None
        # r values type, useful for a literal to a promotable type
        # like long <- int, or double <- float
        self.inferred_type_data = None
        

class FunctionArgsData:
    def __init__(self) -> None:
        self.name_token = None
        self.variable_type_data = None

class StructFieldData:
    def __init__(self) -> None:
        self.field_name_token = None
        self.type_token = None
        self.variable_type_data = None


class VariableTypeData:
    def __init__(self) -> None:
        self.type_name_token = None
        self.is_user_defined = False
        self.type_name = None
        self.is_interface = False
        self.is_struct = False
        self.is_enum = False
        self.is_union = False
        self.is_define_stmt = False
        self.is_primitive = False
        self.is_array = False
        self.is_function = False
        self.is_mutable = False

        self.is_hashable = False
        self.is_comparable = False
        

class Loop_label:
    def __init__(self) -> None:
        self.name_token = None
        self.sequence_number = None
        self.scope_depth = None


class StatementAnalyzer:
    def __init__(self, database, error_manager):
        self.database = database
        self.error_manager = error_manager
        # Sets the order in which statements are analyzed
        # can be confugred in testing utilities to test specific cases
        self.declared_variables = list()
        self.loop_labels = list()
        self.struct_fields = list()
        self.args = list()
        self.function_name_token = None
        self.unittest_name_token = None
        self.struct_object_id = None
        self.fn_or_test_id = None
        self.sequence_number = 0
        self.statements = None
        

    def reset(self):
        self.declared_variables = list()
        self.loop_labels = list()
        self.struct_fields = list()
        self.args = list()
        self.function_name_token = None
        self.unittest_name_token = None
        self.struct_object_id = None
        self.fn_or_test_id = None
        self.sequence_number = 0
        self.statements = None

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)

    def analyze(self, function_or_unittest_object_id, structure_object_id=None):
        function_or_unittest_object = self.database.get_object(function_or_unittest_object_id)
        self.reset()
        self.struct_object_id = structure_object_id
        self.fn_or_test_id = function_or_unittest_object_id
        function_or_unittest_object.accept(self)


    def analyze_function_statements(self, function_object):
        self.statements = function_object.get_statements()
        if self.struct_object_id is not None:
            struct = self.database.get_object(self.struct_object_id)
            struct_fields = struct.get_fields()
            for field in struct_fields:
                field_data = StructFieldData()
                field_data.field_name_token = field.get_name()
                field_data.type_token = field.get_type_name()
                field_data.variable_type_data = self.find_variable_type(field.get_type_name())
                self.struct_fields.append(field_data)

        args = function_object.get_args()
        for arg in args:
            arg_data = FunctionArgsData()
            arg_data.name_token = arg.get_name()
            arg_data.variable_type_data = self.find_variable_type(arg.get_type_name())
            self.args.append(arg_data)
        self.function_name_token = function_object.get_name_token()
        self.analyze_statements()

    def analyze_unittest_statements(self, unittest_object):
        self.statements = unittest_object.get_statements()
        self.unittest_name_token = unittest_object.get_name_token()
        self.analyze_statements()

    def analyze_statements(self, scope_depth=0):
        for statement in self.statements:
            statement.accept(self, scope_depth)



    # let a as int = 0
    # var b as SomeType = some_instance
    def analyze_declaration(self, statement, scope_depth):
        # get name of variable, save it to list of declared variables
        # Lets the expression analyzer check if some variable is using the same name
        # Also, immediately check if there is already a variable with the same name using that list
        self.sequence_number += 1
        variable_data = LocalVariableDeclaration()
        variable_data.name_token = statement.get_name()

        variable_data.mutability_token = statement.get_descriptor_token()
        variable_data.sequence_number = self.sequence_number
        variable_data.scope_depth = scope_depth
        variable_data.statement = statement
        

        for var in self.declared_variables:
            if var.name_token.literal == variable_data.name_token.literal:
                # print("HERE!")
                # print(var.scope_depth, variable_data.scope_depth)
                # print(var.sequence_number, variable_data.sequence_number)
                # print(var.name_token.literal, variable_data.name_token.literal)
                if self.folowing_declaration_in_previous_scope(var, variable_data):
                    self.add_error(
                        variable_data.name_token,
                        ErrMsgs.DUPLICATE_DECLARATION,
                        var.name_token,
                    )

        
        # This code is good, but needs testing / fixing. Test above code first

        print("exp analysis")
        exp_analyzer = ExpressionAnalyzer(self)
        exp_analyzer.analyze(statement.get_expression_ast())
        inferred_type_data = exp_analyzer.get_analysis_result()
        if inferred_type_data is None:
            print("no inferred type data, likely error")
            # Found some kind of semantic error in the expression
            return
        # # This way a variable in the expression will be undeclared if it has the same
        # # name as the variable being declared.
        
        self.declared_variables.append(variable_data)

        type_name_token = None
        if statement.get_type() is not None:
            type_name_token = statement.get_type()
        else:
            # Viola! Type Inference
            print("assigning type name token")
            type_name_token = inferred_type_data.type_token

        if is_primitive_type(type_name_token) or is_boolean_literal(type_name_token):
            print("is primitive type")
            variable_data.variable_type_data = VariableTypeData()
            variable_data.variable_type_data.type_name_token = type_name_token
            variable_data.variable_type_data.is_comparable = True
            variable_data.variable_type_data.is_hashable = True # strings, int, and chars are hashable, but not bools, or floats
            variable_data.variable_type_data.is_primitive = True
            variable_data.variable_type_data.is_mutable = variable_data.mutability_token.literal == VAR
        else:
            variable_data.variable_type_data = self.find_variable_type(type_name_token)

        if type_name_token.get_type() != inferred_type_data.type_token.get_type():
            print(f"Type mismatch: {type_name_token.get_type()} != {inferred_type_data.type_token.get_type()}")
            incompatible_types = True
            if self.r_value_is_promotable_to_l_value_type(type_name_token, inferred_type_data.type_token):
                incompatible_types = False
            elif self.both_are_bools(type_name_token, inferred_type_data.type_token):
                print("both are bools")
                incompatible_types = False
            elif self.r_value_implements_l_value_type_as_interface(type_name_token, inferred_type_data.type_token):
                print("adding error")
                incompatible_types = False
            if incompatible_types:
                self.add_error(
                    type_name_token, ErrMsgs.EXP_VAR_TYPE_MISMATCH, inferred_type_data.type_token
                )

        # Because if the type as stated is wrong,
        # we'll just treat the expression as the true type (because that is the true type anyways)
        variable_data.type_token = type_name_token
        variable_data.inferred_type_data = inferred_type_data

    def analyze_reassignment(statement):
        pass






    def analyze_return_statement(self, statement, scope_depth):
        pass

    def analyze_if_statement(self, statement, scope_depth):
        for statement in statement.get_statements():
            statement.accept(self, scope_depth + 1)

    def analyze_elif_statement(self, statement, scope_depth):
        for statement in statement.get_statements():
            statement.accept(self, scope_depth + 1)

    def analyze_else_statement(self, statement, scope_depth):
        for statement in statement.get_statements():
            statement.accept(self, scope_depth + 1)

    def analyze_unless_statement(self, statement, scope_depth):
        for statement in statement.get_statements():
            statement.accept(self, scope_depth + 1)

    def analyze_function_call(self, statement, scope_depth):
        pass

    def analyze_break_statement(self, statement, scope_depth):
        pass

    def analyze_continue_statement(self, statement, scope_depth):
        pass

    def analyze_while_statement(self, statement, scope_depth):
        pass

    def analyze_forloop_statement(self, statement, scope_depth):
        pass

    def analyze_switch_statement(self, statement, scope_depth):
        pass

    def analyze_defer_statement(self, statement, scope_depth):
        pass


    def r_value_implements_l_value_type_as_interface(self, type_name_token, inferred_type_token) -> bool:
        return False
        # get type of r value, check if it's a struct
        # check type of l value, check if it's an interface
        # check if struct implements interface

    def find_variable_type(self, name_token):
        # returns the token of the declaration of the type (struct, enum, union, define stmt)
        query = ModuleItemsQuery(self.fn_or_test_id)
        module_objects = self.database.execute_query(query)
        imports_query = ImportItemsInModuleQuery(self.fn_or_test_id)
        import_objects = self.database.execute_query(imports_query)
        for obj in module_objects:
            if obj.name_token.literal == name_token.literal:
                return self.variable_type_data_from_module_object(obj)
        
        for obj in import_objects:
            if obj.get_type_name_token().literal == name_token.literal:
                return self.variable_type_data_from_import_object(obj)
        

    def variable_type_data_from_module_object(self, obj):
        # Find out as much as possible about that type
        # check for system methods like __eq__, __hash__, __str__, __repr__
        # or more of a C# or Java named methods like equals, hashcode, tostring etc.
        pass
        table_name = self.database.get_tablename_for_object(obj.object_id)
        if table_name == "structs":
            pass
        elif table_name == "enums":
            pass
        elif table_name == "unions":
            pass
        elif table_name == "defines":
            pass
        elif table_name == "interfaces":
            pass
        # ...
        else:
            raise Exception("INTERNAL ERROR: table name for object id was not found")

    def variable_type_data_from_import_object(self, obj):
        pass


    # Shadowing declaration at same level, or deeper, but only if the shadowing declaration
    # is in the same list of statements, or some substatement of the current list of statements.
    # A seond declaration in a parents siblings sub statements is not a shadowed variable, if that sibling is after the parent.
    def folowing_declaration_in_previous_scope(self, previous_declaration, current_declaration):
        statements_following_previous = self.get_statements_following_declaration(previous_declaration, self.statements)
        if statements_following_previous is None:
            return False
        return self.declaration_in_statements(current_declaration, statements_following_previous)


    def get_statements_following_declaration(self, declaration, statements):
        for i, stmt in enumerate(statements):
            if stmt == declaration.statement:
                return statements[i+1:]
            if stmt.has_nested_statements():
                nested_statements = stmt.get_statements()
                stmt_slice = self.get_statements_following_declaration(declaration, nested_statements)
                if stmt_slice is not None and len(stmt_slice) > 0:
                    return stmt_slice
        return None
    

    def declaration_in_statements(self, declaration, statements):
        for stmt in statements:
            if stmt == declaration.statement:
                return True
            if stmt.has_nested_statements():
                nested_statements = stmt.get_statements()
                if self.declaration_in_statements(declaration, nested_statements):
                    return True

        return False
    

    def r_value_is_promotable_to_l_value_type(self, type_name_token, inferred_type_token):
        if not is_primitive_type(type_name_token):
            return False
        if not is_primitive_type(inferred_type_token):
            return False
        
        if inferred_type_token.get_type() == FLOAT and type_name_token.get_type() == DOUBLE:
            print("float to double")
            return True
        if inferred_type_token.get_type() == INT and type_name_token.get_type() == LONG:
            print("int to long")
            return True
        print("returning false")
        return False

    def both_are_bools(self, type_name_token, inferred_type_token):
        return is_boolean_literal(inferred_type_token) and type_name_token.get_type() == BOOL

