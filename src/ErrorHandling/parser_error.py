class ParserError:
    def __init__(self, token, message, expected_types = None):
        self.token = token
        self.message = message
        self.expected_types = expected_types

    def to_string(self) -> str:
        tok_string = self.message + "\n"
        tok_string += self.token.to_string()
        if self.expected_types:
            tok_string += "possible expected types:\n"
            tok_string += str(self.expected_types)
        return tok_string
    
    def __repr__(self) -> str:
        return self.to_string()