from Parsing.ASTComponents.InternalComponents.assign_statement import AssignmentStatement
from TestingComponents.testing_utilities import token_to_json


class TestingAssignmentStatement:
    def __init__(self):
        self.assign_statement = AssignmentStatement()

    def add_let_or_var(self, let_or_var_token):
        self.assign_statement.add_let_or_var(let_or_var_token)

    def add_name(self, name_token):
        self.assign_statement.add_name(name_token)

    def add_type(self, type_token):
        self.assign_statement.add_type(type_token)

    def add_expression_value(self, exp_ast):
        self.assign_statement.add_expression_value(exp_ast)

    def print_literal(self, repr_list: list) -> None:
        repr_list.append("name: ")
        repr_list.append(self.assign_statement.name_token.literal + ", type: ")
        if self.assign_statement.type_token is not None:
            repr_list.append(self.assign_statement.type_token.literal)
        repr_list.append(", ownership type: " + self.assign_statement.let_or_var_token.literal+ ", ")
        repr_list.append("exp: ")
        self.assign_statement.exp_ast.print_literal(repr_list)

    def print_token_types(self, type_list: list) -> None:
        type_list.append(self.assign_statement.name_token.type_symbol + " ")
        if self.assign_statement.type_token is not None:
            type_list.append(self.assign_statement.type_token.type_symbol + " ")
        type_list.append(self.assign_statement.let_or_var_token.type_symbol + " ")
        self.assign_statement.exp_ast.print_token_types(type_list)

    def to_json(self) -> dict:
        return {
            "type" : "assignment",
            "token" : token_to_json(self.assign_statement.name_token),
            "variable_type" : token_to_json(self.assign_statement.type_token),
            "assignment_type" : token_to_json(self.assign_statement.let_or_var_token),
            "rvalue" : self.assign_statement.exp_ast.to_json()
        }
    
    def add_descriptor_token(self, token):
        self.assign_statement.add_descriptor_token(token)

    def get_descriptor_token(self):
        return self.assign_statement.get_descriptor_token()
