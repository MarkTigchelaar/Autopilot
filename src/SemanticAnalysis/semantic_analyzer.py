from SemanticAnalysis.Database.database import Database

class SemanticAnalyzer:
    def __init__(self, error_manager, database = None):
        self.error_manager = error_manager
        if database is None:
            self.database = Database(error_manager)
        else:
            self.database = database

    def add_error(self, token, message):
        self.error_manager.add_semantic_error(token, message)

    def save_item_to_data_store(self, ast_node_saver):
        ast_node_saver.save_to_db(self.database)

    def analyze_globally(self):
        self.database.process_queries(self)
