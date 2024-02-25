import ErrorHandling.semantic_error_messages as ErrMsg


class FuntionAnalyzer:
    def __init__(self, database, error_manager):
        self.database = database
        self.error_manager = error_manager

    def analyze(self, object_id):
        pass


"""
TODO list:
Check that argument types are defined somewhere
Check that function name has no collisions
Check the variable names are defined in their scope
Check types for argument re assignment
check types of expressions
Check method and function calls
Register current function as caller of any called functions to later check inline / acyclic rules
Check fields and methods of types referenced in function
Check arguments to other functions and methods
Enforce enumerable type rules, like with switch statements for unions
Enforce optional variable rules.
Enforce that collections return Results or Optionals if guarantee of membership is not present
Check that Errors in results have valid fields
Check that break statements that refer to labels have labels that exist
Check that labels have no name collisions
Check assignment types, for let, and var
Check if expressions violate int / float promotion rules
Check that function / method calls are public
"""