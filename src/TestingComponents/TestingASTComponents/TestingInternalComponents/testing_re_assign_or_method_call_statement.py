from Parsing.ASTComponents.InternalComponents.re_assign_or_method_call import ReassignmentOrMethodCall
from TestingComponents.testing_utilities import token_to_json

class TestingReAssignOrMethodCallStatement:
    def __init__(self):
        self.re_assign_or_method_Call_statement = ReassignmentOrMethodCall()

    def add_l_value_exp(self, l_value_exp):
        self.re_assign_or_method_Call_statement.add_l_value_exp(l_value_exp)

    def add_assignment_token(self, assignment_token):
        self.re_assign_or_method_Call_statement.add_assignment_token(assignment_token)

    def add_r_value(self, r_value_exp):
        self.re_assign_or_method_Call_statement.add_r_value(r_value_exp)

    def print_literal(self, repr_list: list) -> None:
        #repr_list.append()
        self.re_assign_or_method_Call_statement.l_value_exp.print_literal(repr_list)
        #repr_list.append(" ")
        if self.re_assign_or_method_Call_statement.assignment_token:
            repr_list.append(" " + self.re_assign_or_method_Call_statement.assignment_token.literal + " ")
        if self.re_assign_or_method_Call_statement.r_value_exp:
            self.re_assign_or_method_Call_statement.r_value_exp.print_literal(repr_list)

    def print_token_types(self, type_list: list) -> None:
        self.re_assign_or_method_Call_statement.l_value_exp.print_token_types(type_list)
        if self.re_assign_or_method_Call_statement.assignment_token:
            type_list.append(" " + self.re_assign_or_method_Call_statement.assignment_token.type_symbol + " ")
        if self.re_assign_or_method_Call_statement.r_value_exp:
            self.re_assign_or_method_Call_statement.r_value_exp.print_token_types(type_list)
    
    def to_json(self) -> dict:
        return {
            "type" : "reassign_or_call",
            "lvalue" : self.re_assign_or_method_Call_statement.l_value_exp.to_json(),
            "assignment_type_token" : token_to_json(self.re_assign_or_method_Call_statement.assignment_token),
            "rvalue" : self.rvalue_to_json()
        }

    def rvalue_to_json(self):
        if self.re_assign_or_method_Call_statement.r_value_exp:
            return self.re_assign_or_method_Call_statement.r_value_exp.to_json()
        else:
            return dict()
