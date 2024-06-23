import ErrorHandling.semantic_error_messages as ErrMsgs
from keywords import is_primitive_type, is_boolean_literal
from symbols import *


from SemanticAnalysis.Database.Queries.module_and_imported_items_from_function_id_query import (
    ModuleAndImportedItemsFromCallerFunctionIdAndCalleeNameQuery,
)
from SemanticAnalysis.Database.Queries.matching_import_item_alias_from_function import (
    MatchingImportItemAliasFromFunction,
)
from SemanticAnalysis.Database.Queries.current_module_id_query import (
    CurrentModuleIdQueryQuery,
)


class ExpressionType:
    def __init__(self, name_or_symbol_token, type_token, variable_type_data=None):
        self.name_or_symbol_token = name_or_symbol_token
        self.type_token = type_token
        self.variable_type_data = variable_type_data
        if self.type_token and self.type_token.get_type() in (BOOL, TRUE, FALSE):
            self.type_token.set_type(BOOL)

    def __str__(self):
        if self.type_token:
            return f"ExpressionType: {self.type_token.literal}"
        else:
            return "ExpressionType: None"


class ExpressionAnalyzer:
    def __init__(self, parent_analyzer):
        self.parent_analyzer = parent_analyzer
        self.expression_type = None
        self.found_Error = False

    def add_error(
        self,
        token,
        message,
        shadowed_token=None,
        lhs_type_token=None,
        rhs_type_token=None,
    ):
        self.found_Error = True
        self.parent_analyzer.error_manager.add_semantic_error(
            token, message, shadowed_token, lhs_type_token, rhs_type_token
        )

    def get_analysis_result(self):
        if self.found_Error:
            return None
        return self.expression_type

    def analyze(self, expression_ast):
        expression_ast.accept(self)

    # These methods are a cleaner way for the analyzer to know which type is involved
    # by using the visitor pattern

    # For struct fields, args, and declared variables, we need to check if the type is user defined
    # if it is, we need to set the is_user_defined flag to True
    # and we need to get the type name type, from its definition
    # These should be figured out
    def visit_name_expression(self, name_expression):
        name_token = name_expression.get_name()
        print(f"analyzing token: {name_token.literal}, {name_token.get_type()}")
        if self.is_primitive(name_token):
            print("Found a primitive in expression")
            self.expression_type = ExpressionType(name_token, name_token)
            return

        for var in self.parent_analyzer.declared_variables:
            if var.name_token.literal == name_token.literal:
                if self.is_primitive(var.type_token):
                    self.expression_type = ExpressionType(name_token, var.type_token)
                else:
                    self.expression_type = ExpressionType(
                        name_token, var.type_token, var.variable_type_data
                    )
                return

        for field in self.parent_analyzer.struct_fields:
            if field.field_name_token.literal == name_token.literal:
                if self.is_primitive(field.type_token):
                    self.expression_type = ExpressionType(name_token, field.type_token)
                else:
                    self.expression_type = ExpressionType(
                        name_token, field.type_token, field.variable_type_data
                    )
                return

        for arg in self.parent_analyzer.args:
            if arg.name_token.literal == name_token.literal:
                if self.is_primitive(arg.type_token):
                    self.expression_type = ExpressionType(name_token, arg.type_token)
                else:
                    self.expression_type = ExpressionType(
                        name_token, arg.type_token, arg.variable_type_data
                    )
                return

        self.add_error(name_token, ErrMsgs.UNDECLARED_EXP_VAR)

    def visit_prefix_expression(self, prefix_expression):
        rhs_expression = prefix_expression.get_rhs_exp()
        rhs_expression.accept(self)
        rhs_type = self.expression_type
        prefix_type_name_token = prefix_expression.get_name()
        if not self.exp_compatible_with_operator(prefix_type_name_token, rhs_type):
            self.add_error(
                rhs_type.name_or_symbol_token,
                ErrMsgs.INVALID_PREFIX_EXP,
                prefix_type_name_token,
                None,
                rhs_type.type_token,
            )
            self.expression_type = None

    # Just like the prefix, but add checks for lhs with operator, and if lhs is compatible with the rhs.
    def visit_binary_operator_expression(self, binary_expression):
        operator_token = binary_expression.get_name()
        found_error = False

        lhs_expression = binary_expression.get_lhs_exp()
        lhs_expression.accept(self)
        lhs_type = self.expression_type
        if lhs_type and (
            not self.exp_compatible_with_binary_operator(operator_token, lhs_type)
        ):
            self.add_error(
                lhs_type.name_or_symbol_token,
                ErrMsgs.INVALID_BINARY_EXP,
                operator_token,
                lhs_type.type_token,
                None,
            )
            found_error = True

        rhs_expression = binary_expression.get_rhs_exp()
        rhs_expression.accept(self)
        rhs_type = self.expression_type
        if rhs_type and (
            not self.exp_compatible_with_binary_operator(operator_token, rhs_type)
        ):
            self.add_error(
                rhs_type.name_or_symbol_token,
                ErrMsgs.INVALID_BINARY_EXP,
                operator_token,
                None,
                rhs_type.type_token,
            )
            found_error = True

        if (lhs_type and rhs_type) and (
            not self.expression_types_compatible(lhs_type, rhs_type)
        ):
            self.add_error(
                lhs_type.name_or_symbol_token,
                ErrMsgs.INCOMPATIBLE_EXPRESSION_TYPES,
                rhs_type.name_or_symbol_token,
                lhs_type.type_token,
                rhs_type.type_token,
            )
            found_error = True

        if found_error:
            self.expression_type = None

    def visit_function_call_expression(self, function_call_expression):
        # is List[TypeRow]
        matching_definitions = self.check_if_function_is_defined(
            function_call_expression.fn_name_exp.get_name()
        )

        return_type = self.check_call_args_against_function_definition(
            matching_definitions, function_call_expression
        )

        # check argument types / number of arguments
        # check it returns something
        # check that it returns the right type
        # done
        if return_type is not None:
            self.expression_type = ExpressionType(
                function_call_expression.fn_name_exp.get_name(), return_type
            )

    def is_primitive(self, token):
        return is_primitive_type(token) or is_boolean_literal(token)

    def exp_compatible_with_operator(self, operator_token, rhs_type):
        if operator_token.type_symbol == MINUS:
            return rhs_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE)
        elif operator_token.type_symbol == NOT:
            return (
                is_boolean_literal(rhs_type.type_token)
                or rhs_type.type_token.get_type() == BOOL
            )
        else:
            print("PREFIX TYPE NOT IMPLEMENTED")
            # Don't remember if there were more, I don't think so
            return False

    def exp_compatible_with_binary_operator(self, operator_token, exp_type):
        if operator_token.type_symbol == PLUS:
            return exp_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE)
        elif operator_token.type_symbol == MINUS:
            return exp_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE)
        elif operator_token.type_symbol == STAR:
            return exp_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE)
        elif operator_token.type_symbol == SLASH:
            return exp_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE)
        elif operator_token.type_symbol == MOD:
            return exp_type.type_token.get_type() in (INT, LONG)
        elif operator_token.type_symbol == CARROT:
            return exp_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE)
        elif operator_token.type_symbol == AND:
            return exp_type.type_token.get_type() == BOOL
        elif operator_token.type_symbol == OR:
            return exp_type.type_token.get_type() == BOOL
        # elif operator_token.type_symbol == NOT:
        #     return exp_type.type_token.get_type() == BOOL
        elif operator_token.type_symbol == NAND:
            return exp_type.type_token.get_type() == BOOL
        elif operator_token.type_symbol == NOR:
            return exp_type.type_token.get_type() == BOOL
        elif operator_token.type_symbol == XOR:
            return exp_type.type_token.get_type() == BOOL
        elif operator_token.type_symbol == EQUAL_EQUAL:
            # if expression type is a user defined type, return true
            # return exp_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE, BOOL)
            return True
        elif operator_token.type_symbol == BANG_EQUAL:
            # if expression type is a user defined type, return true, these will rely on memory addresses
            # so no need for anything special
            # return exp_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE, BOOL)
            return True
        elif operator_token.type_symbol == LESS:
            return exp_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE)
        elif operator_token.type_symbol == LESS_EQUAL:
            return exp_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE)
        elif operator_token.type_symbol == GREATER:
            return exp_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE)
        elif operator_token.type_symbol == GREATER_EQUAL:
            return exp_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE)
        else:
            raise Exception("BINARY TYPE NOT IMPLEMENTED")
            # return False

    def expression_types_compatible(self, lhs_type, rhs_type):
        if lhs_type.type_token.get_type() == rhs_type.type_token.get_type():
            return True
        else:
            return False
        # if one is a user defined type, check if the other is the same type
        # if not, error
        # if both are primitive, check if they are compatible
        # if not, error
        # if one is a primitive and the other is a user defined type, error
        # if both are user defined types, check if they are the same type
        # if not, error

    def check_if_function_is_defined(self, function_name_token):
        function_id = self.parent_analyzer.fn_or_test_id

        items_visible_to_function_query = (
            ModuleAndImportedItemsFromCallerFunctionIdAndCalleeNameQuery(
                function_id, function_name_token.literal
            )
        )
        query_result = self.parent_analyzer.database.execute_query(
            items_visible_to_function_query
        )

        header_id = (
            self.parent_analyzer.database.get_table("functions")
            .get_item_by_id(function_id)
            .header_id
        )

        current_module_id_query = CurrentModuleIdQueryQuery(header_id)
        current_module_id = self.parent_analyzer.database.execute_query(
            current_module_id_query
        ).next()

        all_names_from_matching_alias = self.get_names_for_aliases(
            function_name_token, function_id
        )
        # account for multiple results, and raise ambiguity related errors
        found_items = []
        for item in query_result:
            if item.name_token.literal == function_name_token.literal:
                # must be current module_id
                found_items.append(item)

            else:
                for name_row in all_names_from_matching_alias:
                    # Ensure it is only collecting items where the name matches the alias given in
                    # import statement
                    if item.name_token.literal == name_row.literal:
                        if current_module_id != item.module_id:
                            found_items.append(item)

        if len(found_items) == 0:
            self.add_error(function_name_token, ErrMsgs.FUNCTION_NOT_DEFINED)

        matching_functions = list()
        for found_item in found_items:
            if found_item.category not in ("function", "fn_header"):
                # check for union, struct type names, if so, is constructor
                self.add_error(
                    function_name_token,
                    ErrMsgs.REFERENCED_ITEM_IS_NOT_A_FUNCTION,
                    found_item.name_token,
                )
            else:
                matching_functions.append(found_item)
        return matching_functions  # List[TypeRow]

    def get_names_for_aliases(self, function_name_token, function_id):
        item_import_alias_query = MatchingImportItemAliasFromFunction(
            function_id, function_name_token.literal
        )
        query_result = self.parent_analyzer.database.execute_query(
            item_import_alias_query
        )
        aliases = []
        for row in query_result:
            if row.get_type_name_token().literal == function_name_token.literal:
                aliases.append(row.name_token)
        return list(set(aliases))

    # class TypeRow:
    #     def __init__(self, category, module_id, object_id, name_token):
    #         self.category = category
    #         self.module_id = module_id
    #         self.object_id = object_id
    #         self.name_token = name_token

    def check_call_args_against_function_definition(
        self, matching_definitions, function_call_expression
    ):

        return_type = None
        for matching_definition in matching_definitions:
            # function_object = self.parent_analyzer.database.get_table("functions").get_item_by_id(matching_definition.object_id)
            function_header = self.parent_analyzer.database.get_table(
                "fn_headers"
            ).get_item_by_id(matching_definition.object_id)
            actual_args = function_header.get_args()
            return_type = function_header.get_return_type()
            num_call_args = len(function_call_expression.argument_list)
            num_actual_args = len(actual_args)
            if return_type is None:
                self.add_error(
                    function_call_expression.fn_name_exp.get_name(),
                    ErrMsgs.FUNCTION_CALLED_HAS_NO_RETURN_TYPE,
                    function_header.get_name(),
                    None,
                    None,
                )
            if num_call_args != num_actual_args:
                self.add_error(
                    function_call_expression.fn_name_exp.get_name(),
                    ErrMsgs.FUNCTION_CALL_ARG_NUMBER_MISMATCH,
                    function_header.get_name(),  # function_call_expression.fn_name_exp.get_name(),
                    None,
                    None,
                )

            for arg_index in range(min(num_call_args, num_actual_args)):
                call_arg = function_call_expression.argument_list[arg_index]
                actual_arg = actual_args[arg_index]
                arg_analyzer = ExpressionAnalyzer(self.parent_analyzer)
                if not self.call_arg_type_matches_actual_arg_type(
                    arg_analyzer, call_arg, actual_arg
                ):
                    call_arg_type = arg_analyzer.get_analysis_result()
                    if call_arg_type is not None:
                        shadowed_token = call_arg_type.name_or_symbol_token
                    else:
                        shadowed_token = None
                    self.add_error(
                        shadowed_token,
                        ErrMsgs.FUNCTION_CALL_ARG_TYPE_MISMATCH,
                        actual_arg.get_type(),
                        None,
                        None,
                    )
        return return_type if len(matching_definitions) == 1 else None

    def call_arg_type_matches_actual_arg_type(self, arg_analyzer, call_arg, actual_arg):
        arg_analyzer.analyze(call_arg)
        call_arg_type = arg_analyzer.get_analysis_result()
        if call_arg_type is None:
            return False
        actual_arg_type = actual_arg.get_type()
        if actual_arg_type.get_type() == call_arg_type.type_token.get_type():
            return True
        return False

    def visit_collection_expression(self, collection_expression):
        if self.is_hash_literal(collection_expression):
            self.check_hash_literal(collection_expression)
        elif self.is_list_literal(collection_expression):
            self.check_list_literal(collection_expression)
        else:
            raise Exception("INTERNAL ERROR: COLLECTION TYPE NOT IMPLEMENTED")

    def is_list_literal(self, collection_expression):
        uses_brackets = collection_expression.left_type == LEFT_BRACKET
        return uses_brackets

    def is_hash_literal(self, collection_expression):
        if collection_expression.left_type == LEFT_BRACE:
            return True
        return False

    def check_hash_literal(self, collection_expression):
        colon_count_list = self.count_colons_per_element(collection_expression)
        if sum(colon_count_list) == 0:
            self.check_set_literal(collection_expression)
        else:
            self.check_dict_literal(collection_expression, colon_count_list)

    def check_set_literal(self, collection_expression):
        element_ast_list = collection_expression.get_collection_elements()
        key_type_list = []
        for i in range(len(element_ast_list)):
            key_type_list.append(self.check_element_type(element_ast_list[i]))
        self.check_type_consistancy(key_type_list, ErrMsgs.INCONSISTANT_HASH_ELEMENT_TYPES)
        self.check_key_type_is_hashable(key_type_list, ErrMsgs.UNHASHABLE_HASH_ELEMENT_TYPES)
        

    def check_dict_literal(self, collection_expression, colon_count_list):
        element_ast_list = collection_expression.get_collection_elements()
        key_type_list = []
        value_type_list = []
        for i in range(len(colon_count_list)):
            if colon_count_list[i] > 1:
                self.add_error(
                    element_ast_list[i].get_name(),
                    ErrMsgs.MULTIPLE_MAP_DELIMITERS_FOUND,
                )
            elif colon_count_list[i] == 0:
                self.add_error(
                    element_ast_list[i].get_name(), ErrMsgs.MISSING_MAP_DELIMITER
                )
            else:
                key_type_list.append(self.check_key_type(element_ast_list[i]))
                value_type_list.append(self.check_value_type(element_ast_list[i]))

        self.check_type_consistancy(key_type_list, ErrMsgs.INCONSISTANT_MAP_KEY_TYPES)
        self.check_type_consistancy(value_type_list, ErrMsgs.INCONSISTANT_MAP_VALUE_TYPES)
        self.check_key_type_is_hashable(key_type_list, ErrMsgs.UNHASHABLE_MAP_KEY_TYPES)

    def check_key_type(self, element_ast):
        if element_ast.get_name().get_type() != COLON:
            raise Exception("INTERNAL ERROR: KEY VALUE PARTITION NOT FOUND")
        lhs_analyzer = ExpressionAnalyzer(self.parent_analyzer)
        lhs_analyzer.analyze(element_ast.get_lhs_exp())
        inferred_type_data = lhs_analyzer.get_analysis_result()
        if inferred_type_data is None:
            raise Exception("INTERNAL ERROR: KEY TYPE NOT FOUND")
        return inferred_type_data

    def check_value_type(self, element_ast):
        if element_ast.get_name().get_type() != COLON:
            raise Exception("INTERNAL ERROR: KEY VALUE PARTITION NOT FOUND")
        rhs_analyzer = ExpressionAnalyzer(self.parent_analyzer)
        rhs_analyzer.analyze(element_ast.get_rhs_exp())
        inferred_type_data = rhs_analyzer.get_analysis_result()
        if inferred_type_data is None:
            raise Exception("INTERNAL ERROR: VALUE TYPE NOT FOUND")
        return inferred_type_data

    def check_element_type(self, element_ast):
        analyzer = ExpressionAnalyzer(self.parent_analyzer)
        analyzer.analyze(element_ast)
        inferred_type_data = analyzer.get_analysis_result()
        if inferred_type_data is None:
            raise Exception("INTERNAL ERROR: ELEMENT TYPE NOT FOUND")
        return inferred_type_data


    # List[ExpressionType]
    def check_type_consistancy(self, type_list, error_message):
        first_type = type_list[0].type_token.get_type()
        for i in range(1, len(type_list)):
            if type_list[i].type_token.get_type() != first_type:
                self.add_error(
                    type_list[0].name_or_symbol_token,
                    error_message,
                    type_list[i].name_or_symbol_token,
                    type_list[0].type_token,
                    type_list[i].type_token,
                )

    def check_key_type_is_hashable(self, key_type_list, error_message):
        """
            floats and doubles -> no
            bools -> no
            strings -> yes
            ints and longs -> yes
            structs -> yes (unless inlined, then no)
            unions -> yes (unless inlined, then no)
            enums -> yes, unless bools or floats / doubles (they are just primitive types)
            interfaces -> yes
            anything defined with the define statement -> no
        """
        for key_type in key_type_list:
            if key_type.type_token.get_type() in (FLOAT, DOUBLE) or self.is_defined_type(key_type):
                self.add_error(
                    key_type.name_or_symbol_token,
                    error_message,
                    None,
                    key_type.type_token,
                    None,
                )
        

    def is_defined_type(self, key_type):
        pass
        # lookup the typename, see if it is a type defined in a define statement
        # Refer to previous semantic checks, which already do this (ish)


    def check_list_literal(self, collection_expression):
        element_ast_list = collection_expression.get_collection_elements()
        key_type_list = []
        for i in range(len(element_ast_list)):
            key_type_list.append(self.check_element_type(element_ast_list[i]))
        self.check_type_consistancy(key_type_list, ErrMsgs.INCONSISTANT_LIST_ELEMENT_TYPES)

    def count_colons_per_element(self, collection_expression):
        colons_found_list = []
        for item in collection_expression.get_collection_elements():
            colons_found = self.count_colons_in_exp(item)
            colons_found_list.append(colons_found)
        return colons_found_list

    def count_colons_in_exp(self, item):
        count = int(item.get_name().get_type() == COLON)
        if item.has_left_expression():
            count += self.count_colons_in_exp(item.left_expression)
        if item.has_right_expression():
            count += self.count_colons_in_exp(item.right_expression)
        return count

    def visit_method_call_or_field_expression(self, method_or_field_expression):
        # check if the method or field exists
        # check if the arguments are compatible with the method, will rely on function call expression
        # set the expression type to the return type of the method, also done by function call expression
        pass

    def visit_collection_access_expression(self, collection_access_expression):
        # check if collection exists
        # check if the index is a valid type, also check if it is a loop variable
        # if so, collection returns contained type, else returns a result.
        # check if the collection is a valid type, like can you return something from it
        # set the expression type to the type of the collection's value
        pass




"""
    TODO: typechecking with user defined types like define stmt, or structs / unions etc.
    finish hashing check. All hashing done with primitives or items memory address, so anything on the heap which is not in a define statement.
"""