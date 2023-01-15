class TokenizerError:
    def __init__(self, token, message):
        self.token = token
        self.message = message

    def to_string(self):
        err = self.message + "\n"
        err += self.token.to_string()
        return err