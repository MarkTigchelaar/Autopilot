


class ReturnStatement:
    def __init__(self):
        self.expression = None
    
    def add_expression(self, exp_ast):
        self.expression = exp_ast
