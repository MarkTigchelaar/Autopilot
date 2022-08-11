class SwitchStatementAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        return
    end
end

class CaseStatementAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        return
    end
end
