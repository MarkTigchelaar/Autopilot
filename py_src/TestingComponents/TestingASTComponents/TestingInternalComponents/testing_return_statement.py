from Parsing.ASTComponents.InternalComponents.return_statement import ReturnStatement


class TestingReturnStatement:
    def __init__(self):
        self.return_statement = ReturnStatement()

    def add_expression(self, exp_ast):
        self.return_statement.add_expression(exp_ast)

    def print_literal(self, repr_list: list) -> None:
        self.return_statement.expression.print_literal(repr_list)

    def print_token_types(self, type_list: list) -> None:
        self.return_statement.expression.print_token_types(type_list)

    def to_json(self) -> dict:
        return {
            "type" : "return",
            "expression" : self.expression_to_json()
        }

    def expression_to_json(self):
        if self.return_statement.expression:
            return self.return_statement.expression.to_json()
