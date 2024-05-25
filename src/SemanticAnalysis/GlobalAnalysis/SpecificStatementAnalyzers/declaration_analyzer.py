import ErrorHandling.semantic_error_messages as ErrMsg
from SemanticAnalysis.GlobalAnalysis.SpecificStatementAnalyzers.specific_statement_analyzer import SpecificStatementAnalyzer
from SemanticAnalysis.Database.Queries.statement_data_query import ContainerData

class DeclarationAnalyzer(SpecificStatementAnalyzer):
    def analyze(self, container_data: ContainerData):
        #self.check_if_variables_are_defined()
        declarations = self.get_declarations(container_data)
        for i in range(len(declarations)):
            for j in range(i, len(declarations)):
                if declarations[i].name == declarations[j].name and i != j:
                    self.add_error(declarations[i].token, ErrMsg.DUPLICATE_DECLARATION, declarations[j].token)


    def get_declarations(self, container_data: ContainerData):
        # make query to get all the declarations in the container
        return []
