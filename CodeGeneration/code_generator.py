from abc import ABC, abstractmethod
from typing import List

from ASTComponents.AggregatedComponents.modules import RawModule

#LINE_CHAR_LIMIT = 100

class CodeGenerator(ABC):
    def __init__(self, raw_modules: List[RawModule]):
        self.raw_modules = raw_modules
        self.output_code_lines = list()
        self.line_in_progress = []
        self.indent_level = 0

    def increase_indent_level(self):
        self.indent_level += 4

    def decrease_indent_level(self):
        self.indent_level -= 4

    def get_indent_whitespace(self) -> str:
        return ' ' * self.indent_level if self.indent_level > 0 else ''
    

    def add_to_current_line_w_space(self, item: str):
        self.add_to_current_line(item + ' ')

    def add_to_current_line(self, item: str):
        self.line_in_progress.append(item)

    def consolidate_line(self) -> str:
        return ''.join(self.line_in_progress)
    
    def begin_line(self):
        self.add_to_current_line(self.get_indent_whitespace())

    def complete_line(self):
        self.output_code_lines.append(self.consolidate_line())
        self.line_in_progress.clear()

    # def line_length_beyond_char_limit(self) -> bool:
    #     return len(self.consolidate_line()) > LINE_CHAR_LIMIT

    @abstractmethod
    def generate_code(self): pass


    @abstractmethod
    def trigger_output(self) : pass
