


class SwitchStatement:
    def __init__(self):
        self.test_expression = None
        self.case_statements = list()
        self.default_case = None
        self.descriptor_token = None
    
    def add_test_expression(self, test_exp):
        self.test_expression = test_exp
    
    def add_case(self, case):
        self.case_statements.append(case)

    def get_statements(self):
        return self.case_statements
    
    def add_default_case(self, default):
        self.default_case = default

    def has_default_case(self):
        return self.default_case is not None

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token
    
    def has_nested_statements(self):
        return True

class CaseStatement:
    def __init__(self):
        self.values = list()
        self.statements = None
        self.descriptor_token = None

    def add_value(self, value):
        self.values.append(value)

    def add_statements(self, statement_list):
        self.statements = statement_list

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token
    
    def get_statements(self):
        return self.statements

    def has_nested_statements(self):
        return True
