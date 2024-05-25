import ErrorHandling.semantic_error_messages as ErrMsgs
from keywords import is_primitive_type, is_boolean_literal
from symbols import *


class ExpressionType:
    def __init__(self, name_or_symbol_token, type_token, variable_type_data=None):
        self.name_or_symbol_token = name_or_symbol_token
        self.type_token = type_token
        self.variable_type_data = variable_type_data

    def __str__(self):
        return f"ExpressionType: {self.type_token.literal}"


class ExpressionAnalyzer:
    def __init__(self, parent_analyzer):
        self.parent_analyzer = parent_analyzer
        self.expression_type = None
        self.found_Error = False

    def add_error(self, token, message, shadowed_token=None):
        self.found_Error = True
        self.parent_analyzer.error_manager.add_semantic_error(
            token, message, shadowed_token
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
                    self.expression_type = ExpressionType(
                        name_token, var.type_token
                    )
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

    def visit_binary_operator_expression(self, binary_expression):
        pass
        # literally just go through the left and right expressions and return the type for each by capturing the expression
        # by keeping them as local variables until the method returns
        # binary_expression.get_lhs_exp.accept(self)
        # lhs_value = self.expression_type
        # binary_expression.get_rhs_exp.accept(self)
        # rhs_value = self.expression_type
        # operator_token = binary_expression.get_operator()

    def visit_prefix_expression(self, prefix_expression):
        pass

    def visit_function_call_expression(self, function_call_expression):
        pass

    def visit_collection_access_expression(self, collection_access_expression):
        pass

    def visit_collection_expression(self, collection_expression):
        pass

    def visit_method_call_or_field_expression(self, method_or_field_expression):
        pass

    def is_primitive(self, token):
        return is_primitive_type(token) or is_boolean_literal(token)
