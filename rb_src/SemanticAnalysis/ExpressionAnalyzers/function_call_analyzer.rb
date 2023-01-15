class FunctionCallExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        args = ast_node.getArguments()
        for arg_expression in args do
            @main_analyzer.analyze_node_locally(arg_expression)
        end
        # still need name collisions, unresolved references to types / identifiers etc.
    end
end
