

class LoopStatement:
    def __init__(self):
        self.loop_name = None
        self.statements = None

    def add_loop_name(self, loop_name):
        self.loop_name = loop_name

    def add_statements(self, statements):
        self.statements = statements
