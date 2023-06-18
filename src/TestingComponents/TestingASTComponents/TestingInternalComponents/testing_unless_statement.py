from Parsing.ASTComponents.InternalComponents.unless_statement import UnlessStatement
from TestingComponents.testing_utilities import token_to_json

class TestingUnlessStatement:
    def __init__(self):
        self.unless_statement = UnlessStatement()

    def add_descriptor_token(self, token):
        self.unless_statement.add_descriptor_token(token)

    def get_descriptor_token(self):
        return self.unless_statement.get_descriptor_token()

    def add_expression(self, exp_ast):
        self.unless_statement.add_expression(exp_ast)

    def add_statements(self, statements):
        self.unless_statement.add_statements(statements)

    def print_literal(self, repr_list: list) -> None:
        self.unless_statement.test_expression.print_literal(repr_list)
        if self.unless_statement.statements:
            for stmt in self.unless_statement.statements:
                stmt.print_literal(repr_list)
        
    def print_token_types(self, type_list: list) -> None:
        self.unless_statement.test_expression.print_token_types(type_list)
        if self.unless_statement.statements:
            for stmt in self.unless_statement.statements:
                stmt.print_literal(type_list)

    def to_json(self) -> dict:
        return {
            "type" : "unless",
            "expression" : self.unless_statement.test_expression.to_json(),
            "statememts" : self.statements_to_json()
        }
    
    def statements_to_json(self):
        stmts = list()
        for stmt in self.unless_statement.statements:
            stmts.append(stmt.to_json())
        return stmts
