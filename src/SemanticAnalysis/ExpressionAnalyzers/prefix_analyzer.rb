class PrefixExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        @main_analyzer.analyze_node_locally(ast_node.getRhsExp())
        operator = ast_node.getName()
        exp_type = @main_analyzer.getExpressionTypeToken()
        unless @main_analyzer.astSubTreeCompatableWithOperator(operator)
            msg = "Operator \"#{operator.getText()}\" cannot be applied to expression of type \"#{exp_type.getType().downcase()}\""
            make_and_send_error(ast_node.getName(), msg)
        end
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
