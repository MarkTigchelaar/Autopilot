

class SemanticError:
    def __init__(self, token, message):
        self.token = token
        self.message = message

    def to_string(self) -> str:
        tok_string = self.message + "\n"
        tok_string += self.token.to_string()
        return tok_string
