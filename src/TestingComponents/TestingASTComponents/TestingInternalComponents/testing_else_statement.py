from Parsing.ASTComponents.InternalComponents.else_statement import ElseStatement

class TestingElseStatement:
    def __init__(self):
        self.else_statement = ElseStatement()
    
    def add_statements(self, statements):
        self.else_statement.add_statements(statements)

    def print_literal(self, repr_list: list) -> None:
        if self.else_statement.statements:
            for stmt in self.else_statement.statements:
                stmt.print_literal(repr_list)
        
    def print_token_types(self, type_list: list) -> None:
        if self.else_statement.statements:
            for stmt in self.else_statement.statements:
                stmt.print_literal(type_list)

    def to_json(self) -> dict:
        return {
            "type" : "else",
            "statememts" : self.statements_to_json()
        }
    
    def statements_to_json(self):
        stmts = list()
        for stmt in self.else_statement.statements:
            stmts.append(stmt.to_json())
        return stmts

    def add_descriptor_token(self, token):
        self.else_statement.add_descriptor_token(token)

    def get_descriptor_token(self):
        return self.else_statement.get_descriptor_token()