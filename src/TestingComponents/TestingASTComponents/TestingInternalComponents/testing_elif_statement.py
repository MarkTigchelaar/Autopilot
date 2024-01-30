from ASTComponents.InternalComponents.elif_statement import ElifStatement
from TestingComponents.testing_utilities import token_to_json


class TestingElifStatement:
    def __init__(self):
        self.elif_statement = ElifStatement()

    def add_descriptor_token(self, token):
        self.elif_statement.add_descriptor_token(token)

    def get_descriptor_token(self):
        return self.elif_statement.get_descriptor_token()

    def add_expression(self, exp_ast):
        self.elif_statement.add_expression(exp_ast)

    def add_assignment_type(self, assign_type_token):
        self.elif_statement.add_assignment_type(assign_type_token)

    def add_variable_name(self, variable_token):
        self.elif_statement.add_variable_name(variable_token)

    def add_optional_name(self, option_name_token):
        self.elif_statement.add_optional_name(option_name_token)

    def add_statements(self, statements):
        self.elif_statement.add_statements(statements)

    def add_next_statement_in_block(self, statement):
        self.elif_statement.add_next_statement_in_block(statement)

    def print_literal(self, repr_list: list) -> None:
        self.elif_statement.test_expression.print_literal(repr_list)
        if self.elif_statement.optional_assignment_type:
            repr_list.append(self.elif_statement.optional_assignment_type.literal)
            repr_list.append(
                self.elif_statement.unwrapped_optional_variable_name.literal
            )
            repr_list.append(self.elif_statement.optional_variable_name.literal)
        if self.elif_statement.statements:
            for stmt in self.elif_statement.statements:
                stmt.print_literal(repr_list)

    def print_token_types(self, type_list: list) -> None:
        self.elif_statement.test_expression.print_token_types(type_list)
        if self.elif_statement.optional_assignment_type:
            type_list.append(self.elif_statement.optional_assignment_type.type_symbol)
            type_list.append(
                self.elif_statement.unwrapped_optional_variable_name.type_symbol
            )
            type_list.append(self.elif_statement.optional_variable_name.type_symbol)
        if self.elif_statement.statements:
            for stmt in self.elif_statement.statements:
                stmt.print_literal(type_list)

    def to_json(self) -> dict:
        return {
            "type": "elif",
            "assignment_type": token_to_json(
                self.elif_statement.optional_assignment_type
            ),
            "unwrapped_option": token_to_json(
                self.elif_statement.unwrapped_optional_variable_name
            ),
            "option": token_to_json(self.elif_statement.optional_variable_name),
            "expression": self.elif_statement.test_expression.to_json(),
            "statememts": self.statements_to_json(),
            "next_stmt_in_block": self.block_stmt_to_json(),
        }

    def statements_to_json(self):
        stmts = list()
        for stmt in self.elif_statement.statements:
            stmts.append(stmt.to_json())
        return stmts

    def block_stmt_to_json(self):
        if self.elif_statement.next_statement_in_block:
            return self.elif_statement.next_statement_in_block.to_json()
        return dict()
