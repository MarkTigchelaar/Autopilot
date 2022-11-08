class ReturnAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        return_expression = ast_node.get_ast()
        unless return_expression.nil?
            @main_analyzer.analyze_node_locally(return_expression)
        end
    end
end
