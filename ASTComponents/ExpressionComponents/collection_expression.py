class CollectionExpression:
    def __init__(self):
        # brackets, currly braces etc.
        self.left_type: str = None
        self.expression_array = None
        self.rhs_type: str = None
        # The general type(s) of the collection
        self.key_type = None # Token
        self.value_type = None
        self.is_map_type = None


    def add_lhs_type(self, lhs_type):
        self.left_type = lhs_type

    def get_lhs_type(self):
        return self.left_type

    def is_hash_type(self):
        if self.left_type != "LEFT_BRACE":
            return False
        for exp in self.expression_array:
            if self.dig_for_map_indicator_token(exp):
                return True
        return False
    
    def is_list_type(self):
        return self.left_type == "["
    

    
    def add_expression(self, expression_array):
        self.expression_array = expression_array

    def get_collection_elements(self):
        return self.expression_array
    
    def add_rhs_type(self, rhs_type):
        self.rhs_type = rhs_type


    def set_types_of_collection(self, key_type, value_type):
        self.key_type = key_type
        self.value_type = value_type

    def set_type(self, _type):
        self.key_type = _type
    
    def get_type(self):
        return self.key_type
    
    def get_value_type(self):
        return self.value_type

    # def accept(self, expression_analyzer):
    #     expression_analyzer.analyze_collection_literal_expression(self)

    def has_left_expression(self):
        return False

    def has_right_expression(self): 
        return False


    def dig_for_map_indicator_token(self, exp):
        if exp.has_left_expression():
            if self.dig_for_map_indicator_token(exp.get_lhs_exp()):
                return True
        if exp.has_right_expression():
            if self.dig_for_map_indicator_token(exp.get_rhs_exp()):
                return True
        if exp.token.literal == ":":
            return True
        return False
    
    def accept_resolved_statement(self, type_annotater):
        return type_annotater.make_collection_expression(self)