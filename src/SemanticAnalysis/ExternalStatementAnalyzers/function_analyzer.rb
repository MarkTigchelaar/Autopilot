class FunctionAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        stmts = ast_node.get_statements()
        @main_analyzer.analyze_node_locally(stmts)
    end
end
