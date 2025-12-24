from ErrorHandling.semantic_error import SemanticError

class SemanticErrorManager:
    def __init__(self):
        self.errors = []
        self.organized = False

    def add_error(self, token, message, shadowed_token = None, lhs_type_token = None, rhs_type_token = None) -> None:
        semantic_error = SemanticError(token, message, shadowed_token, lhs_type_token, rhs_type_token)
        self.errors.append(semantic_error)


    def has_errors(self) -> bool:
        """
        Check if there are any parsing errors.

        :return: True if there are errors, False otherwise.
        """
        return len(self.errors) > 0
    


    def get_errors(self) -> list:
        """
        Get the list of parsing errors.

        :return: A list of tuples containing line numbers and error messages.
        """
        return self.errors
    
    def get_next_error(self):
        self.organize()
        if len(self.errors) == 0:
            return None
        return self.errors.pop()

    def organize(self):
        if self.organized:
            return
        self.errors.reverse()
        self.organized = True