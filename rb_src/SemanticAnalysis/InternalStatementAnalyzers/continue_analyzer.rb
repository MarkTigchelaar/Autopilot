class ContinueAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        return
        # just need to check if inside a loop, see break analyzer
    end
end
