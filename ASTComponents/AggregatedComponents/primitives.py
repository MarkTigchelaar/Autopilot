from Tokenization.symbols import INT, LONG, FLOAT, DOUBLE, CHAR, STRING, BOOL, NULL


class PrimitiveType:
    def __init__(self, internal_type_symbol):
        self.internal_type_symbol = internal_type_symbol

    def get_internal_type_symbol(self):
        if self.internal_type_symbol is None:
            raise Exception("Missing internal type symbol")
        return self.internal_type_symbol

class Integer(PrimitiveType):
    def __init__(self):
        super().__init__(INT)

class Long(PrimitiveType):
    def __init__(self):
        super().__init__(LONG)

class Float(PrimitiveType):
    def __init__(self):
        super().__init__(FLOAT)

class Double(PrimitiveType):
    def __init__(self):
        super().__init__(DOUBLE)

class Char(PrimitiveType):
    def __init__(self):
        super().__init__(CHAR)

class String(PrimitiveType):
    def __init__(self):
        super().__init__(STRING)

class Bool(PrimitiveType):
    def __init__(self):
        super().__init__(BOOL)


class Null(PrimitiveType):
    def __init__(self):
        super().__init__(NULL)