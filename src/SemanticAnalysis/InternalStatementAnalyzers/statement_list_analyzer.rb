class StatementListAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        for statement in ast_node.getStatements() do
            @main_analyzer.analyze_node_locally(statement)
        end
    end
end
