from typing import Union

# Designed to be used for 1 source only
class SourceScanner:
    def __init__(self, read_string = False):
        self.is_complete = False
        self.src = None
        self.line_number = 1
        self.column_number = 0
        self.current_token_col_start = 0
        self.buffer = None
        self._peek_char = None
        self.is_reading_string = read_string

    def load_src(self, file_name_or_string) -> None:
        if self.is_reading_string:
            self.src = StringReader(file_name_or_string)
        else:
            self.src = FileReader(file_name_or_string)
    
    def close_src(self) -> None:
        self.src.close()

    def get_column_number(self) -> int:
        return self.column_number

    def peek_char(self) -> str:
        if self._peek_char is None:
            self._peek_char = self.advance_one()
        return self._peek_char

    def read_char(self) -> Union[str, None]:
        if self._peek_char is not None:
            self.add_to_buffer(self._peek_char)
            temp = self._peek_char
            self.inc_position(self._peek_char)
            self._peek_char = None
            return temp
        char = self.advance_one()
        if char:
            self.inc_position(char)
            self.add_to_buffer(char)
            return char
        else:
            self.close_src()
            self.is_complete = True
            return None

    def add_to_buffer(self, char) -> None:
        if self.buffer:
            self.buffer += char 
        else:
            self.buffer = "" + char

    def advance_one(self) -> Union[str, None]:
        if self.is_complete:
            return None
        char = self.src.read()
        if char == '':
            self.is_complete = True
            return None
        else:
            return char

    def get_buffer(self) -> str:
        return self.buffer

    def clear_buffer(self) -> None:
        self.buffer = None
        self.set_token_start_col_number()

    def complete(self) -> bool:
        if self.is_complete:
            self.close_src()
        return self.is_complete

    def set_token_start_col_number(self) -> None:
        self.current_token_col_start = self.column_number

    def inc_position(self, char: str) -> None:
        if char in ('\n', '\r'):
            self.line_number += 1
            self.column_number = 0
            self.current_token_col_start = 0
        elif char == '\t':
            self.column_number += 2
        else:
            self.column_number += 1


class StringReader:
    def __init__(self, src_string: str):
        self.src = list(src_string)
        self.current = 0

    def read(self) -> str:
        if self.current < len(self.src):
            temp = self.src[self.current]
            self.current += 1
            return temp
        return ''

    def close(self) -> None:
        return

class FileReader:
    def __init__(self, file_name: str):
        self.src_file = open(file_name, "r")
        self.is_open = True

    def read(self) -> str:
        if not self.is_open:
            raise Exception("INTERNALL ERROR: attempted to read file that is no longer open")
        return self.src_file.read(1)

    def close(self) -> None:
        if self.is_open:
            self.src_file.close()
