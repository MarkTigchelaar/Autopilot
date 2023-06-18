from ErrorHandling.semantic_error_messages import *

# switch name
#   case 'b', 'c', d do
#    var a = 6
#   default 
#     let a = 0
# end
def analyze_switch(analyzer, ast_node):
    cases = ast_node.case_statements
    for i in range(len(cases)):
        check_values_in_case_stmt_for_dups(analyzer, cases[i])
        for j in range(i + 1):
            check_values_in_other_case_stmt_for_dups(analyzer, cases[i], cases[j])


def check_values_in_case_stmt_for_dups(analyzer, case):
    for i in range(len(case.values)):
        for j in range(i + 1):
            if case.values[i].literal == case.values[j].literal:
                analyzer.add_error(case.values[j], DUPLICATE_CASE_VALUE)


def check_values_in_other_case_stmt_for_dups(analyzer, case_one, case_two):
    for val_one in case_one.values:
        for val_two in case_two.values:
            if val_one.literal == val_two.literal:
                analyzer.add_error(val_two, DUPLICATE_CASE_VALUE)

