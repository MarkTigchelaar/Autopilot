from Parsing.ASTComponents.InternalComponents.if_statement import IfStatement
from TestingComponents.testing_utilities import token_to_json


class TestingIfStatement:
    def __init__(self):
        self.if_statement = IfStatement()

    def add_descriptor_token(self, token):
        self.if_statement.add_descriptor_token(token)

    def get_descriptor_token(self):
        return self.if_statement.get_descriptor_token()

    def add_expression(self, exp_ast):
        self.if_statement.add_expression(exp_ast)

    def add_assignment_type(self, assign_type_token):
        self.if_statement.add_assignment_type(assign_type_token)

    def add_variable_name(self, variable_token):
        self.if_statement.add_variable_name(variable_token)

    def add_optional_name(self, option_name_token):
        self.if_statement.add_optional_name(option_name_token)

    def add_statements(self, statements):
        self.if_statement.add_statements(statements)

    def add_next_statement_in_block(self, statement):
        self.if_statement.add_next_statement_in_block(statement)

    def print_literal(self, repr_list: list) -> None:
        self.if_statement.test_expression.print_literal(repr_list)
        if self.if_statement.optional_assignment_type:
            repr_list.append(self.if_statement.optional_assignment_type.literal)
            repr_list.append(self.if_statement.unwrapped_optional_variable_name.literal)
            repr_list.append(self.if_statement.optional_variable_name.literal)
        if self.if_statement.statements:
            for stmt in self.if_statement.statements:
                stmt.print_literal(repr_list)

    def print_token_types(self, type_list: list) -> None:
        self.if_statement.test_expression.print_token_types(type_list)
        if self.if_statement.optional_assignment_type:
            type_list.append(self.if_statement.optional_assignment_type.type_symbol)
            type_list.append(
                self.if_statement.unwrapped_optional_variable_name.type_symbol
            )
            type_list.append(self.if_statement.optional_variable_name.type_symbol)
        if self.if_statement.statements:
            for stmt in self.if_statement.statements:
                stmt.print_literal(type_list)

    def to_json(self) -> dict:
        return {
            "type": "if",
            "assignment_type": token_to_json(
                self.if_statement.optional_assignment_type
            ),
            "unwrapped_option": token_to_json(
                self.if_statement.unwrapped_optional_variable_name
            ),
            "option": token_to_json(self.if_statement.optional_variable_name),
            "expression": self.if_statement.test_expression.to_json(),
            "statememts": self.statements_to_json(),
            "next_stmt_in_block": self.block_stmt_to_json(),
        }

    def statements_to_json(self):
        stmts = list()
        for stmt in self.if_statement.statements:
            stmts.append(stmt.to_json())
        return stmts

    def block_stmt_to_json(self):
        if self.if_statement.next_statement_in_block:
            return self.if_statement.next_statement_in_block.to_json()
        return dict()
