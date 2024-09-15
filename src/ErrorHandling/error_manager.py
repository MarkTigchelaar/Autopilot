from .tokenizer_error import TokenizerError
from .parser_error import ParserError
from .semantic_error import SemanticError

# This class is used for the entire compilation process,
# but only for one thread. If multi threaded, the compiler 
# will have one instance of these per thread.
class ErrorManager:
    def __init__(self):
        self.tokenizer_errors: list[TokenizerError] = list()
        self.parser_errors: list[ParserError] = list()
        self.semantic_errors = list()
        self.organized = False

    def has_errors(self, include_semantic_errors = False) -> bool:
        if len(self.tokenizer_errors) > 0:
            return True
        elif len(self.parser_errors) > 0:
            return True
        elif len(self.semantic_errors) > 0 and include_semantic_errors:
            return True
        return False

    def add_tokenizer_error(self, token, message: str) -> None:
        tok_error = TokenizerError(token, message)
        self.tokenizer_errors.append(tok_error)

    def next_tokenizer_error(self) -> TokenizerError:
        if not self.organized:
            self.organize()
        if len(self.tokenizer_errors) < 1:
            raise Exception("INTERNAL ERROR: tokenizer error list empty")
        return self.tokenizer_errors.pop()

    def add_parser_error(self, token, message, expected_types = None) -> None:
        parser_error = ParserError(token, message, expected_types)
        self.parser_errors.append(parser_error)

    def next_parser_error(self) -> ParserError:
        if not self.organized:
            self.organize()
        if len(self.parser_errors) < 1:
            raise Exception("INTERNAL ERROR: parse error list empty")
        return self.parser_errors.pop()

    def add_semantic_error(self, token, message, shadowed_token = None, lhs_type_token = None, rhs_type_token = None) -> None:
        semantic_error = SemanticError(token, message, shadowed_token, lhs_type_token, rhs_type_token)
        self.semantic_errors.append(semantic_error)

    def next_semantic_error(self) -> SemanticError:
        if not self.organized:
            self.organize()
        if len(self.semantic_errors) < 1:
            raise Exception("INTERNAL ERROR: semantic error list empty")
        return self.semantic_errors.pop()

    def next_error(self):
        if len(self.tokenizer_errors) > 0:
            return self.tokenizer_errors.pop()
        if len(self.parser_errors) > 0:
            return self.parser_errors.pop()
        if len(self.semantic_errors) > 0:
            return self.semantic_errors.pop()
        return None
    
    def get_errors(self):
        self.organize()
        return self.tokenizer_errors + self.parser_errors + self.semantic_errors

    def organize(self) -> None:
        # to pop errors from the back, not front
        self.tokenizer_errors.reverse()
        self.parser_errors.reverse()
        self.semantic_errors.reverse()
        self.organized = True


    def report_errors(self):
        self.organize()
        for error in self.tokenizer_errors:
            print(error)
        for error in self.parser_errors:
            print(error)
        for error in self.semantic_errors:
            print(error)
