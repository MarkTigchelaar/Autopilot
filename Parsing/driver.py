from Tokenization.tokenizer import Tokenizer
from ErrorHandling.parser_error_manager import ParsingErrorManager


class Driver:
    def __init__(
        self, tokenizer: Tokenizer, err_manager: ParsingErrorManager, testing=False
    ):
        self.err_manager = err_manager
        self.tokenizer = tokenizer
        self.modifier_container = None
        self.testing = testing

    def current_file(self):
        return self.tokenizer.current_file()

    def add_error(self, token, err_message):
        self.err_manager.add_error(token, err_message)

    def has_errors(self):
        return self.err_manager.has_errors()

    def discard_token(self):
        self.tokenizer.next_token()

    def get_modifier_container(self):
        if self.modifier_container is None:
            self.modifier_container = ModifierContainer()
        return self.modifier_container

    def delete_modifier_container(self):
        self.modifier_container = None

    def next_token(self):
        return self.tokenizer.next_token()

    def peek_token(self):
        return self.tokenizer.peek_next_token()

    def is_unit_testing(self) -> bool:
        return self.testing


class ModifierContainer:
    def __init__(self):
        self.public_token = None
        self.inline_token = None
        self.acyclic_token = None

    def add_public_token(self, token):
        self.public_token = token

    def add_inline_token(self, inline_token):
        self.inline_token = inline_token

    def add_acyclic_token(self, token):
        self.acyclic_token = token

    def get_public_token(self):
        return self.public_token

    def get_inline_token(self):
        return self.inline_token

    def get_acyclic_token(self):
        return self.acyclic_token
