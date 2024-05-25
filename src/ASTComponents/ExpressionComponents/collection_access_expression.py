
class CollectionAccessExpression:
    def __init__(self):
        self.collection_name_exp = None
        self.argument_list = None

    def add_name_exp(self, collection_name_exp):
        self.collection_name_exp = collection_name_exp

    def add_argument_list(self, argument_list):
        self.argument_list = argument_list

    def accept(self, expression_analyzer):
        expression_analyzer.visit_collection_access_expression(self)
