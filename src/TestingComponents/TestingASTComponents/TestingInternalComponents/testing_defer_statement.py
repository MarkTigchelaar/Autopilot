from Parsing.ASTComponents.InternalComponents.defer_statement import DeferStatement
from TestingComponents.testing_utilities import token_to_json


class TestingDeferStatement:
    def __init__(self):
        self.defer_statement = DeferStatement()
    
    def add_reassignment_statement(self, re_assign_stmt):
        self.defer_statement.add_reassignment_statement(re_assign_stmt)
    