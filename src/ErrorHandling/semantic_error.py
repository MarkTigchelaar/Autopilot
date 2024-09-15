

class SemanticError:
    def __init__(self, token, message, shadowed_token, lhs_type_token, rhs_type_token):
        self.token = token
        self.message = message
        self.shadowed_token = shadowed_token
        self.lhs_type_token = lhs_type_token
        self.rhs_type_token = rhs_type_token

    def to_string(self) -> str:
        tok_string = self.message + "\n"
        tok_string += self.token.to_string()
        if self.shadowed_token:
            tok_string += self.shadowed_token.to_string()
        if self.lhs_type_token:
            tok_string += self.lhs_type_token.to_string()
        if self.rhs_type_token:
            tok_string += self.rhs_type_token.to_string()
        return tok_string
    

    def __repr__(self) -> str:
        return self.to_string()
