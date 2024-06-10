import ErrorHandling.semantic_error_messages as ErrMsgs
from keywords import is_primitive_type, is_boolean_literal
from symbols import *


class ExpressionType:
    def __init__(self, name_or_symbol_token, type_token, variable_type_data=None):
        self.name_or_symbol_token = name_or_symbol_token
        self.type_token = type_token
        self.variable_type_data = variable_type_data
        if self.type_token.get_type() in (BOOL, TRUE, FALSE):
            self.type_token.set_type(BOOL)

    def __str__(self):
        return f"ExpressionType: {self.type_token.literal}"


class ExpressionAnalyzer:
    def __init__(self, parent_analyzer):
        self.parent_analyzer = parent_analyzer
        self.expression_type = None
        self.found_Error = False

    def add_error(self, token, message, shadowed_token=None, lhs_type_token=None, rhs_type_token=None):
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
                rhs_type.type_token
            )
            self.expression_type = None

    # Just like the prefix, but add checks for lhs with operator, and if lhs is compatible with the rhs.
    def visit_binary_operator_expression(self, binary_expression):
        operator_token = binary_expression.get_name()
        found_error = False

        lhs_expression = binary_expression.get_lhs_exp()
        lhs_expression.accept(self)
        lhs_type = self.expression_type
        if lhs_type and (not self.exp_compatible_with_binary_operator(operator_token, lhs_type)):
            self.add_error(
                lhs_type.name_or_symbol_token,
                ErrMsgs.INVALID_BINARY_EXP,
                operator_token,
                lhs_type.type_token,
                None
            )
            found_error = True


        rhs_expression = binary_expression.get_rhs_exp()
        rhs_expression.accept(self)
        rhs_type = self.expression_type
        if rhs_type and (not self.exp_compatible_with_binary_operator(operator_token, rhs_type)):
            self.add_error(
                rhs_type.name_or_symbol_token,
                ErrMsgs.INVALID_BINARY_EXP,
                operator_token,
                None,
                rhs_type.type_token
            )
            found_error = True

        
        if (lhs_type and rhs_type) and (not self.expression_types_compatible(lhs_type, rhs_type)):
            self.add_error(
                lhs_type.name_or_symbol_token,
                ErrMsgs.INCOMPATIBLE_EXPRESSION_TYPES,
                rhs_type.name_or_symbol_token,
                lhs_type.type_token,
                rhs_type.type_token
            )
            found_error = True
        
        if found_error:
            self.expression_type = None

    def visit_function_call_expression(self, function_call_expression):
        # find the function in the global scope, or error
        # check if the arguments are compatible with the function
        # set the expression type to the return type of the function
        # return
        pass

    def visit_collection_access_expression(self, collection_access_expression):
        # check if collection exists
        # check if the index is a valid type, also check if it is a loop variable
        # if so, collection returns contained type, else returns a result.
        # check if the collection is a valid type, like can you return something from it
        # set the expression type to the type of the collection's value
        pass

    def visit_collection_expression(self, collection_expression):
        # for collection literals, check if the types are compatible
        # if not, error
        pass

    def visit_method_call_or_field_expression(self, method_or_field_expression):
        # check if the method or field exists
        # check if the arguments are compatible with the method, will rely on function call expression
        # set the expression type to the return type of the method, also done by function call expression
        pass

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
            #return exp_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE, BOOL)
            return True
        elif operator_token.type_symbol == BANG_EQUAL:
            # if expression type is a user defined type, return true, these will rely on memory addresses
            # so no need for anything special
            #return exp_type.type_token.get_type() in (INT, LONG, FLOAT, DOUBLE, BOOL)
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
            #return False

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
        
