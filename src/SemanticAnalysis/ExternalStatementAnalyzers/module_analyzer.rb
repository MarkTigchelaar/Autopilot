class ModuleAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        # nothing to do for local analysis
        return
    end
end
