class PrefixExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        @main_analyzer.analyze_node_locally(ast_node.getRhsExp())
        operator = ast_node.getOperator()
        unless @main_analyzer.astSubTreeCompatableWithOperator(operator)
            msg = "Operator cannot be applied to expression"
            make_and_send_error(ast_node.getName(), msg)
        end
        # might not need to set expression type, since operator, (if compatible) keep the sub trees type
        # unless it's a binary operator, in that case != <= etc take numbers, returns bool
    end

    def make_and_send_error(field_one, message)
        err = Hash.new()
        err["file"] = field_one.getFilename()
        err["tokenLiteral"] = field_one.getText()
        err["lineNumber"] = field_one.getLine()
        err["message"] = message
        @main_analyzer.add_semantic_error(err)
    end
end
