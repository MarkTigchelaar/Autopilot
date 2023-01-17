from Parsing.ASTComponents.InternalComponents.loop_statement import LoopStatement
from TestingComponents.testing_utilities import token_to_json

class TestingLoopStatement:
    def __init__(self):
        self.loop_statement = LoopStatement()

    def add_loop_name(self, loop_name):
        self.loop_statement.add_loop_name(loop_name)

    def add_statements(self, statements):
        self.loop_statement.add_statements(statements)

    def print_literal(self, repr_list: list) -> None:
        if self.loop_statement.loop_name:
            repr_list.append(self.loop_statement.loop_name)
        if self.loop_statement.statements:
            for stmt in self.loop_statement.statements:
                stmt.print_literal(repr_list)
        
    def print_token_types(self, type_list: list) -> None:
        if self.loop_statement.loop_name:
            type_list.append(self.loop_statement.loop_name)
        if self.loop_statement.statements:
            for stmt in self.loop_statement.statements:
                stmt.print_token_types(type_list)

    def to_json(self) -> dict:
        return {
            "type" : "loop",
            "name" : token_to_json(self.loop_statement.loop_name),
            "statememts" : self.statements_to_json()
        }
    
    def statements_to_json(self):
        stmts = list()
        for stmt in self.loop_statement.statements:
            stmts.append(stmt.to_json())
        return stmts
