from SemanticAnalysis.Database.Queries.statement_data_query import ContainerData

# This file contains the abstract class for specific statement analyzers.
class SpecificStatementAnalyzer:
    def __init__(self, parent_analyzer):
        self.parent_analyzer = parent_analyzer

    def analyze(self, container_data: ContainerData):
        raise NotImplementedError("analyze method not implemented")
    
    def add_error(self, token, message, shadowed_token=None):
        self.parent_analyzer.add_error(token, message, shadowed_token)
    
