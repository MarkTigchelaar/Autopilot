import ErrorHandling.semantic_error_messages as ErrMsg


class StatementAnalyzer:
    def __init__(self, database, error_manager):
        self.database = database
        self.error_manager = error_manager
        self.container_object_id = None


    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)


    def analyze(self, container_object_id):
        self.container_object_id = container_object_id
        self.set_container_type()
        statements_table = self.database.get_table("statements")
        statements = statements_table.get_rows_by_container_id(self.container_object_id)
        self.check_if_variables_are_defined(statements)

    
    def set_container_type(self):
        container_type = self.database.get_tablename_for_object(self.container_object_id)
        if container_type not in ("functions", "unittests"):
            raise Exception("INTERNAL ERROR: container type is not a function or unittest")
        self.container_type = container_type

    
    def check_if_variables_are_defined(self, statements):
        declarations = self.get_declarations(statements)
        self.check_for_shadowing_declarations(statements)
        variables = self.get_variables(statements)
        matched = False
        for variable in variables:
            if self.declaration_matched(variable, declarations):
                matched = True
                break
        if not matched:
            self.add_error(
                ErrMsg.UNDEFINED_VARIABLE,
                self.container_object_id
            )
        

    def get_declarations(self, statements):
        declarations = []
        for statement in statements:
            if statement.statement.get_descriptor_token() == "declaration":
                declarations.append(statement.statement)
            if statement.has_nested_statements():
                declarations.extend(self.get_declarations(statement.get_statements()))
        return declarations
    
    def get_variables(self, statements):
        variables = []
        for statement in statements:
            if statement.statement.get_descriptor_token() == "variable":
                variables.append(statement.statement)
            if statement.has_nested_statements():
                variables.extend(self.get_variables(statement.get_statements()))
        return variables

    def declaration_matched(self, variable, declarations):
        # if name matches, and is later statement id, and is in same or deeper scope, then it is defined
        for declaration in declarations: # <- this is bs generated code, but is the general idea
            if variable == declaration:
                return True
        # self.add_error(
        #     variable.,
        #     ErrMsg.UNDEFINED_VARIABLE
        # )
        return False

    def check_for_shadowing_declarations(self, statements):
        pass
        # for statement in statements:
        #     if statement.statement.get_descriptor_token() == "declaration":
        #         if self.is_shadowing(statement):
        #             self.error_manager.add_error(
        #                 ErrMsg.SHADOWING_DECLARATION,
        #                 self.container_object_id
        #             )
        #     if statement.has_nested_statements():
        #         self.check_for_shadowing_declarations(statement.get_statements())