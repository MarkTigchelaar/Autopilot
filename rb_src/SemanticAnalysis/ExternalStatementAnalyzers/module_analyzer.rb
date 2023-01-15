class ModuleAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        @main_analyzer.set_current_module(ast_node.getName())
        # main analyzer should remember which directory it has seen a module name
        # if current directory is not the same -> name collision
    end
end
