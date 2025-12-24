from ErrorHandling.tokenizer_error import TokenizerError


class TokenizerErrorManager:
    """
    This class is responsible for managing errors that occur during tokenization.
    It provides methods to handle and report errors.
    """

    def __init__(self):
        self.errors = []
        self.organized = False

    def add_error(self, token, error_message):
        """
        Adds an error message to the list of errors.

        :param error_message: The error message to be added.
        """
        error = TokenizerError(token, error_message)
        self.errors.append(error)

    def get_errors(self):
        """
        Returns the list of errors.

        :return: A list of error messages.
        """
        return self.errors

    def get_next_error(self):
        self.organize()
        if len(self.errors) == 0:
            return None
        return self.errors.pop()

    def has_errors(self) -> bool:
        """
        Clears the list of errors.
        """
        return len(self.errors) > 0

    def organize(self) -> None:
        if self.organized:
            return
        self.errors.reverse()
        self.organized = True
