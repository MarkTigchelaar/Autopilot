

class NameExpression:
    def __init__(self):
        self.token = None
    
    def add_name(self, name_token):
        self.token = name_token

    def get_name(self):
        return self.token

    def accept(self, expression_analyzer):
        expression_analyzer.visit_name_expression(self)

    def has_left_expression(self):
        return False
    
    def has_right_expression(self): 
        return False
