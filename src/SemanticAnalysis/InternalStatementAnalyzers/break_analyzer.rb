class BreakAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        return
        # main analyzer needs to know if it's currently in a loop, use this to check,
        # also, loop name must be registered
    end
end
