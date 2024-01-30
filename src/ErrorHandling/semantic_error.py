

class SemanticError:
    def __init__(self, token, message, shadowed_token):
        self.token = token
        self.message = message
        self.shadowed_token = shadowed_token

    def to_string(self) -> str:
        tok_string = self.message + "\n"
        tok_string += self.token.to_string()
        if self.shadowed_token:
            tok_string += self.shadowed_token.to_string()
        return tok_string
