
class Token:
    def __init__(self, type_symbol: str, literal: str, file_name: str, line_number: int, column_number: int):
        self.type_symbol = type_symbol
        self.literal = literal
        self.file_name = file_name
        self.line_number = line_number
        self.column_number = column_number

    def get_type(self) -> str:
        return self.type_symbol
    
    def get_name(self):
        return self.literal
    
    def set_type(self, type_symbol: str) -> None:
        self.type_symbol = type_symbol

    def to_string(self) -> str:
        repr = "Token:\n"
        repr += " file: " + self.file_name + "\n"
        repr += " line number: " + str(self.line_number) + "\n"
        repr += " column number: " + str(self.column_number) + "\n"
        repr += " literal: " + self.literal + "\n"
        repr += " type: " + self.type_symbol + "\n"
        return repr
    

    def __str__(self) -> str:
        return self.to_string()
    
