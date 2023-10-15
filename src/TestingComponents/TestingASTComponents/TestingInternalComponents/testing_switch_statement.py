from Parsing.ASTComponents.InternalComponents.switch_statement import SwitchStatement, CaseStatement
from TestingComponents.testing_utilities import token_to_json

class TestingSwitchStatement:
    def __init__(self):
        self.switch_statement = SwitchStatement()

    def add_descriptor_token(self, token):
        self.switch_statement.add_descriptor_token(token)

    def get_descriptor_token(self):
        return self.switch_statement.get_descriptor_token()

    def add_test_expression(self, test_exp):
        self.switch_statement.add_test_expression(test_exp)
    
    def add_case(self, case):
        self.switch_statement.add_case(case)
    
    def add_default_case(self, default):
        self.switch_statement.add_default_case(default)

    def has_default_case(self):
        return self.switch_statement.has_default_case()

    def print_literal(self, repr_list: list) -> None:
        self.switch_statement.test_expression.print_literal(repr_list)
        repr_list.append(" ")
        for case_stmt in self.switch_statement.case_statements:
            case_stmt.print_literal(repr_list)

    def print_token_types(self, type_list: list) -> None:
        self.switch_statement.test_expression.print_token_types(type_list)
        type_list.append(" ")
        for case_stmt in self.switch_statement.case_statements:
            case_stmt.print_token_types(type_list)

    def to_json(self) -> dict:
        return {
            "type" : "switch",
            "test_expression" : self.switch_statement.test_expression.to_json(),
            "cases" : self.cases_to_json(),
            "default_case" : self.default_case_to_json()
        }

    def cases_to_json(self):
        case_list = list()
        for stmt in self.switch_statement.case_statements:
            case_list.append(stmt.to_json())
        return case_list

    def default_case_to_json(self):
        if self.switch_statement.default_case:
            return self.switch_statement.default_case.to_json()
        return dict()

class TestingCaseStatement:
    def __init__(self):
        self.case_statement = CaseStatement()
    
    def add_value(self, value):
        self.case_statement.add_value(value)

    def add_statements(self, statement_list):
        self.case_statement.add_statements(statement_list)

    def add_descriptor_token(self, token):
        self.case_statement.add_descriptor_token(token)

    def print_literal(self, repr_list: list) -> None:
        for value in self.case_statement.values:
            repr_list.append(value.literal + " ")

    def print_token_types(self, type_list: list) -> None:
        for value in self.case_statement.values:
            type_list.append(value.type_symbol + " ")

    def to_json(self) -> dict:
        return {
            "values" : self.values_to_json(),
            "statements" : self.statements_to_json()
        }

    def values_to_json(self):
        values = list()
        for val in self.case_statement.values:
            values.append(token_to_json(val))
        return values

    def statements_to_json(self):
        statements = list()
        for stmt in self.case_statement.statements:
            statements.append(stmt.to_json())
        return statements
