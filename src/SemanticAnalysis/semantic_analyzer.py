class SemanticAnalyzer:
    def __init__(self, error_manager):
        self.error_manager = error_manager

    def add_error(self, token, message):
        self.error_manager.add_semantic_error(token, message)

    def save_item_to_data_store(self, ast_node):
        pass
