class DefineAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        old_name = ast_node.get_old_type()
        new_name = ast_node.get_new_name_token()
    end
end
