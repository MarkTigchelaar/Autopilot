


class SwitchStatement:
    def __init__(self):
        self.test_expression = None
        self.case_statements = list()
        self.default_case = None
        self.descriptor_token = None
    
    def add_test_expression(self, test_exp):
        self.test_expression = test_exp

    def get_test_expression(self):
        return self.test_expression
    
    def add_case(self, case):
        self.case_statements.append(case)

    def get_statements(self):
        stmts = [stmt for stmt in self.case_statements]
        if self.default_case is not None:
            stmts.append(self.default_case)
        return stmts
    
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
    
    def has_next_statement_in_block(self):
        return False
    
    def accept(self, visitor, scope_depth):
        visitor.analyze_switch_statement(self, scope_depth)



class EnumReference:
    def __init__(self, enum_name, field):
        self.enum_name = enum_name
        self.field = field

    def get_enum_name(self):
        return self.enum_name

    def get_field(self):
        return self.field

class CaseStatement:
    def __init__(self):
        self.values = list()
        self.enum_references = list()
        self.statements = None
        self.descriptor_token = None

    def add_value(self, value):
        self.values.append(value)

    def add_enum_reference(self, enum_name, field):
        self.enum_references.append(EnumReference(enum_name, field))

    def has_enum_references(self):
        return len(self.enum_references) > 0

    def get_enum_references(self):
        return self.enum_references

    def get_values(self):
        return self.values

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

    def has_next_statement_in_block(self):
        return False
