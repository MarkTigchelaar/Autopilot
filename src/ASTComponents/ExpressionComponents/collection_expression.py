

class CollectionExpression:
    def __init__(self):
        self.left_type = None
        self.expression_array = None
        self.rhs_type = None

    def add_lhs_type(self, lhs_type):
        self.left_type = lhs_type
    
    def add_expression(self, expression_array):
        self.expression_array = expression_array

    def get_collection_elements(self):
        return self.expression_array
    
    def add_rhs_type(self, rhs_type):
        self.rhs_type = rhs_type

    def accept(self, expression_analyzer):
        expression_analyzer.visit_collection_expression(self)

    def has_left_expression(self):
        return False

    def has_right_expression(self): 
        return False
