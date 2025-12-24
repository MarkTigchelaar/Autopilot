from ErrorHandling.parser_error import ParserError
from Tokenization.token import Token

class ParsingErrorManager:
    """
    A class to manage parsing errors in a structured way.
    """

    def __init__(self):
        self.errors = []
        self.organized = False

    def add_error(self, token: Token, message: str, expected_types: list = None):
        parser_error = ParserError(token, message, expected_types)
        self.errors.append(parser_error)


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