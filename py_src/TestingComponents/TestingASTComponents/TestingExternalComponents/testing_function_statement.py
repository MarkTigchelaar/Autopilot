from Parsing.ASTComponents.ExternalComponents.function_statement import FunctionStatement
from TestingComponents.testing_utilities import token_to_json




class TestingFunctionStatement:
    def __init__(self):
        self.function_statement = FunctionStatement()

    def add_header(self, header):
        self.function_statement.add_header(header)
    
    def add_statements(self, statements):
        self.function_statement.add_statements(statements)

    def add_acyclic_token(self, acyclic_token):
        self.function_statement.add_acyclic_token(acyclic_token)
    
    def add_inline_token(self, inline_token):
        self.function_statement.add_inline_token(inline_token)
    
    def add_public_token(self, pub_token):
        self.function_statement.add_public_token(pub_token)

    def print_literal(self, repr_list: list) -> None:
        if self.function_statement.acyclic_token:
            repr_list.append(self.function_statement.acyclic_token.literal + " ")
        if self.function_statement.inline_token:
            repr_list.append(self.function_statement.inline_token.literal + " ")
        if self.function_statement.pub_token:
            repr_list.append(self.function_statement.pub_token.literal + " ")
        self.function_statement.header.print_literal(repr_list)

    def print_token_types(self, type_list: list) -> None:
        if self.function_statement.acyclic_token:
            type_list.append(self.function_statement.acyclic_token.type_symbol + " ")
        if self.function_statement.inline_token:
            type_list.append(self.function_statement.inline_token.type_symbol + " ")
        if self.function_statement.pub_token:
            type_list.append(self.function_statement.pub_token.type_symbol + " ")
        self.function_statement.header.print_token_types(type_list)

    def to_json(self) -> dict:
        return {
            "type" : "function",
            "header" : self.function_statement.header.to_json(),
            "attributes" : {
                "acyclic" : token_to_json(self.function_statement.acyclic_token),
                "public" : token_to_json(self.function_statement.pub_token),
                "inline" : token_to_json(self.function_statement.inline_token)
            },
            "statements" : self.statements_json_list()
        }

    def statements_json_list(self) -> list:
        statement_list = list()
        for statement in self.function_statement.statements:
            statement_list.append(statement.to_json())
        return statement_list
