


class ModuleDependencyError:
    def __init__(self, message, import_statement_token_dependency_chain):
        self.message = message
        self.import_statement_token_dependency_chain = import_statement_token_dependency_chain

