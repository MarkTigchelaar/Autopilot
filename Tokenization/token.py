

class Token:
    def __init__(self):
        self.literal = None
        self.internal_type = None
        self.instance_type = None
        self.file_name = None
        self.file_path = None
        self.line_number = None
        self.column_number = None

    def to_string(self) -> str:
        return str(self.__dict__)
    
    def __repr__(self):
        return self.to_string()