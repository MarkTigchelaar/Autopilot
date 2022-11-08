require_relative '.\if_analyzer.rb'

class ElifAnalyzer < IfAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        super(ast_node)
    end
end
