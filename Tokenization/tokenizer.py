from Tokenization.source_file_scanner import SourceFileScanner
from Tokenization.token import Token
from Tokenization.utils import (
    is_alpha,
    is_digit,
    is_alpha_numeric,
    is_special_char,
    get_file_path_and_file_name,
    keyword_literal_to_symbol_map,
)
from Tokenization import symbols
from ErrorHandling.tokenizer_error_messages import (
    INVALID_FLOAT,
    EMPTY_CHAR,
    INVALID_ESCAPE_CHAR,
    OPEN_CHAR,
    OPEN_COMMENT,
    OPEN_STRING,
)
from ErrorHandling.tokenizer_error_manager import TokenizerErrorManager
from typing import Union


class Tokenizer:
    def __init__(self, err_manager: TokenizerErrorManager, reading_string=False):
        self.src_scanner = SourceFileScanner(reading_string)
        self.current_token = None
        self.src_file_name = None
        self.error_manager = err_manager

        self.path_to_remove = ""
        self.done = False
        self.tokens = list()
        self.current_index = 0

    def tokenize_file(self, file_name) -> None:
        self.load_src(file_name)
        self.run()
        self.close_src()

    def get_tokens(self) -> list:
        return self.tokens

    def remove_path(self, path):
        self.path_to_remove = path

    def load_src(self, file_name) -> None:
        if self.done:
            raise Exception("INTERNAL ERROR - Tokenizer already used")
        self.src_file_name = file_name
        self.src_scanner.load_src(file_name)

    def current_file(self) -> str:
        return self.src_file_name

    def run(self) -> None:
        while self.has_tokens():
            self.get_token()
            if self.error_manager.has_errors():
                self.tokens = []
                return
            self.tokens.append(self.current_token)
            self.current_token = None
        if self.tokens[-1].internal_type != symbols.EOF:
            self.end_of_file_token()
            self.tokens.append(self.current_token)
            self.current_token = None

    def close_src(self) -> None:
        self.src_scanner.close_src()
        self.done = True

    def has_tokens(self) -> bool:
        return not self.src_scanner.complete()

    # next token immediately returns current token, no save
    def next_token(self) -> Union[Token, None]:
        temp = None
        if self.current_index >= len(self.tokens):
            self.current_index = len(self.tokens) - 1
            temp = self.tokens[self.current_index]
        else:
            temp = self.tokens[self.current_index]
        self.current_index += 1
        return temp
        

    # peek next token saves, and returns current token
    def peek_next_token(self) -> Union[Token, None]:
        return self.tokens[self.current_index]

    def end_of_file_token(self) -> None:
        self.add_token(symbols.EOF)
        self.current_token.literal = ""

    def get_token(self) -> None:
        while self.current_token is None:
            if self.error_manager.has_errors():
                break
            self.scan_for_token()

    def scan_for_token(self) -> None:
        char = self.read_char()
        if char is None:
            self.end_of_file_token()
            return
        elif char in (" ", "\t", "\n", "\r"):
            self.clear_buffer()
            return
        else:
            self.src_scanner.set_token_start_col_number()

        if char == "(":
            self.add_token(symbols.LEFT_PAREN)
        elif char == ")":
            self.add_token(symbols.RIGHT_PAREN)
        elif char == ",":
            self.add_token(symbols.COMMA)
        elif char == "[":
            self.add_token(symbols.LEFT_BRACKET)
        elif char == "]":
            self.add_token(symbols.RIGHT_BRACKET)
        elif char == "{":
            self.add_token(symbols.LEFT_BRACE)
        elif char == "}":
            self.add_token(symbols.RIGHT_BRACE)
        elif char == ":":
            self.add_token(symbols.COLON)
        elif char == ".":
            if self.peek_char() == ".":
                self.shift_right()
                self.add_token(symbols.RANGE)
            else:
                self.add_token(symbols.DOT)
        elif char == "=":
            if self.peek_char() == "=":
                self.shift_right()
                self.add_token(symbols.EQUAL_EQUAL)
            else:
                self.add_token(symbols.EQUAL)
        elif char == "+":
            if self.peek_char() == "=":
                self.shift_right()
                self.add_token(symbols.PLUS_EQUAL)
            else:
                self.add_token(symbols.PLUS)
        elif char == "-":
            if self.peek_char() == "=":
                self.shift_right()
                self.add_token(symbols.MINUS_EQUAL)
            else:
                self.add_token(symbols.MINUS)
        elif char == "*":
            if self.peek_char() == "=":
                self.shift_right()
                self.add_token(symbols.STAR_EQUAL)
            else:
                self.add_token(symbols.STAR)
        elif char == "/":
            self.add_slash_type_token()
        elif char == "^":
            if self.peek_char() == "=":
                self.shift_right()
                self.add_token(symbols.CARROT_EQUAL)
            else:
                self.add_token(symbols.CARROT)
        elif char == "%":
            if self.peek_char() == "=":
                self.shift_right()
                self.add_token(symbols.MOD_EQUAL)
            else:
                self.add_token(symbols.MOD)
        elif char == "!" and self.peek_char() == "=":
            self.shift_right()
            self.add_token(symbols.BANG_EQUAL)
        elif char == "<":
            if self.peek_char() == "=":
                self.shift_right()
                self.add_token(symbols.LESS_EQUAL)
            else:
                self.add_token(symbols.LESS)
        elif char == ">":
            if self.peek_char() == "=":
                self.shift_right()
                self.add_token(symbols.GREATER_EQUAL)
            else:
                self.add_token(symbols.GREATER)
        elif is_alpha(char) or is_special_char(char):
            self.add_identifier_token()
        elif char == "'":
            self.add_char_token()
        elif char == '"':
            self.add_string_token()
        elif is_digit(char):
            self.add_number_token()
        else:
            raise Exception("INTERNAL ERROR - Unknown char: " + char)

    def add_token(self, token_type) -> None:
        token_type_override_map = keyword_literal_to_symbol_map()
        literal = self.src_scanner.get_buffer()
        if literal in token_type_override_map:
            token_type = token_type_override_map[literal]
        full_file_name = self.current_file()
        line_number = self.src_scanner.line_number
        token_column_number = self.src_scanner.current_token_col_start
        self.current_token = Token()

        file_path, file_name = get_file_path_and_file_name(full_file_name)

        self.current_token.literal = literal
        self.current_token.internal_type = token_type
        self.current_token.instance_type = symbols.UNKNOWN_TYPE
        self.current_token.file_name = file_name
        self.current_token.file_path = file_path
        self.current_token.line_number = line_number
        self.current_token.column_number = token_column_number
        self.src_scanner.clear_buffer()

    def add_identifier_token(self) -> None:
        while is_alpha_numeric(self.peek_char()) or is_special_char(self.peek_char()):
            self.shift_right()
        self.add_token(symbols.IDENTIFIER)

    def add_number_token(self) -> None:
        while is_digit(self.peek_char()):
            self.shift_right()
        is_float = False
        if self.peek_char() == ".":
            self.shift_right()
            if is_digit(self.peek_char()):
                is_float = True
                while is_digit(self.peek_char()):
                    self.shift_right()
            else:
                self.add_error(INVALID_FLOAT)
                return

        if is_float:
            f32 = self.src_scanner.get_buffer()
            parts = f32.split(".")
            if (
                len(parts[1]) > 7
            ):  # basically a "good enough for now", could be updated laeter
                self.add_token(symbols.DOUBLE)
            else:
                self.add_token(symbols.FLOAT)
        else:
            min_i32 = -2147483648
            max_i32 = 2147483647
            as_int = int(self.src_scanner.get_buffer())
            if as_int <= max_i32 and as_int >= min_i32:
                self.add_token(symbols.INT)
            else:
                self.add_token(symbols.LONG)

    def add_char_token(self) -> None:
        if self.peek_char() == "'":
            self.add_error(EMPTY_CHAR)
            return
        if self.peek_char() == "\\":
            self.shift_right()
            char = self.read_char()
            if char not in ("\\", "'", '"', "t", "n"):
                self.add_error(INVALID_ESCAPE_CHAR)
                return
        else:
            self.shift_right()
        char = self.read_char()
        if char != "'":
            self.add_error(OPEN_CHAR)
            return
        self.add_token(symbols.CHAR)

    def add_slash_type_token(self) -> None:
        peek_char = self.peek_char()
        if peek_char == "/":
            while self.has_tokens() and self.peek_char() not in ("\n", "\r"):
                self.shift_right()
            self.shift_right()
            self.clear_buffer()
        elif peek_char == "*":
            self.multi_line_comment()
        elif peek_char == "=":
            self.shift_right()
            self.add_token(symbols.SLASH_EQUAL)
        else:
            self.add_token(symbols.SLASH)

    def multi_line_comment(self) -> None:
        self.shift_right()
        comments_section = 1
        while self.has_tokens():
            current = self.read_char()
            peek = self.peek_char()

            if current == "/" and peek == "*":
                comments_section += 1
                self.shift_right()
                self.shift_right()
                current = self.read_char()
                peek = self.peek_char()

            if current == "*" and peek == "/":
                comments_section -= 1
                self.shift_right()

            if comments_section <= 0:
                break
        if comments_section > 0:
            self.add_error(OPEN_COMMENT)
            return
        self.clear_buffer()

    def add_string_token(self) -> None:
        while self.has_tokens():
            current = self.read_char()
            if current == "\\":
                if self.peek_char() == '"':
                    self.shift_right()
            elif current == '"':
                break
        if not self.has_tokens():
            self.add_error(OPEN_STRING)
            return
        self.add_token(symbols.STRING)

    def peek_char(self) -> Union[str, None]:
        return self.src_scanner.peek_char()

    def read_char(self) -> Union[str, None]:
        return self.src_scanner.read_char()

    def shift_right(self) -> None:
        self.read_char()

    def clear_buffer(self) -> None:
        self.src_scanner.clear_buffer()

    def shift_right_discard(self) -> None:
        self.src_scanner.clear_buffer()
        self.read_char()

    def add_error(self, message) -> None:
        self.src_scanner.is_complete = True
        full_file_name = self.current_file()
        file_path, file_name = get_file_path_and_file_name(full_file_name)

        err = Token()
        err.literal = symbols.ERROR
        err.internal_type = symbols.ERROR
        err.instance_type = symbols.UNKNOWN_TYPE
        err.file_name = file_name
        err.file_path = file_path
        err.line_number = self.src_scanner.line_number
        err.column_number = self.src_scanner.current_token_col_start
        self.error_manager.add_error(err, message)
