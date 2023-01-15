class LoopAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        statements = ast_node.get_statements()
        @main_analyzer.analyze_node_locally(statements)
        # name = ast_node.get_name()
        # no action needed, just register name, if present, and register that analyzer is in loop
    end
end
