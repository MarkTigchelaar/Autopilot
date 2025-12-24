class NameExpression:
    def __init__(self):
        self.token = None
        self.type = None
    
    def add_name(self, name_token):
        self.token = name_token

    def get_name(self):
        return self.token

    def accept(self, expression_analyzer):
        expression_analyzer.analyze_name_expression(self)

    def set_type(self, _type):
        self.type = _type

    def get_type(self):
        return self.type

    def has_left_expression(self):
        return False
    
    def has_right_expression(self): 
        return False
    
    def accept_resolved_statement(self, type_annotater):
        return type_annotater.make_name_expression(self)