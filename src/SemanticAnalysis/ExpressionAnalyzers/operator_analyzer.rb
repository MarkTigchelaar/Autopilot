class OperatorExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        @main_analyzer.analyze_node_locally(ast_node.getRhsExp())
        rhsType = @main_analyzer.getExpressionTypeToken()
        operator = ast_node.getOperator()
        unless @main_analyzer.astSubTreeCompatableWithOperator(operator)
            msg = "Operator cannot be applied to expression"
            make_and_send_error(ast_node.getName(), msg)
        end
        @main_analyzer.analyze_node_locally(ast_node.getLhsExp())
        lhsType = @main_analyzer.getExpressionTypeToken()
        unless @main_analyzer.astSubTreeCompatableWithOperator(operator)
            msg = "Operator cannot be applied to expression"
            make_and_send_error(ast_node.getName(), msg)
        end
    end
end
