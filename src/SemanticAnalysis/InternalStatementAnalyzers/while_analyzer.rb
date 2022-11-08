class WhileLoopAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        @main_analyzer.analyze_node_locally(ast_node.get_ast())
        exp_type_tok = @main_analyzer.getExpressionTypeToken()
        if ![BOOL, TRUE, FALSE].include?(exp_type.getType())
            msg = "expression does not resolve to a bool"
            make_and_send_error(exp_type_tok, msg)
        end
        # name = ast_node.get_name()
        statements = ast_node.get_statements()
        @main_analyzer.analyze_node_locally(statements)
    end
end
