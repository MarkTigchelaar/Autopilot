from ASTComponents.InternalComponents.while_statement import WhileStatement
from TestingComponents.testing_utilities import token_to_json

class TestingWhileStatement:
    def __init__(self):
        self.while_statement = WhileStatement()

    def add_descriptor_token(self, token):
        self.while_statement.add_descriptor_token(token)

    def get_descriptor_token(self):
        return self.while_statement.get_descriptor_token()

    def add_expression(self, exp_ast):
        self.while_statement.add_expression(exp_ast)

    def add_loop_name(self, loop_name):
        self.while_statement.add_loop_name(loop_name)

    def add_statements(self, statements):
        self.while_statement.add_statements(statements)

    def print_literal(self, repr_list: list) -> None:
        self.while_statement.test_expression.print_literal(repr_list)
        repr_list.append(" ")
        if self.while_statement.loop_name:
            repr_list.append(self.while_statement.loop_name.literal)
        if self.while_statement.statements:
            for stmt in self.while_statement.statements:
                stmt.print_literal(repr_list)
        
    def print_token_types(self, type_list: list) -> None:
        self.while_statement.test_expression.print_token_types(type_list)
        type_list.append(" ")
        if self.while_statement.loop_name:
            type_list.append(self.while_statement.loop_name.type_symbol + " ")
        if self.while_statement.statements:
            for stmt in self.while_statement.statements:
                stmt.print_token_types(type_list)

    def to_json(self) -> dict:
        return {
            "type" : "while_loop",
            "name" : token_to_json(self.while_statement.loop_name),
            "expression" : self.while_statement.test_expression.to_json(),
            "statememts" : self.statements_to_json()
        }
    
    def statements_to_json(self):
        stmts = list()
        for stmt in self.while_statement.statements:
            stmts.append(stmt.to_json())
        return stmts
