class ReturnAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        return_expression = ast_node.get_ast()
        unless return_expression.nil?
            @main_analyzer.analyze_node_locally(return_expression)
        end
        function_return_type = @main_analyzer.get_return_type()
        expression_type = @main_analyzer.getExpressionTypeToken()
        if return_expression.nil? && !function_return_type.nil?
            msg = "Type error: function expected to return #{function_return_type.getType().downcase()}, but return type found to be empty"
            make_and_send_error(ast_node.get_return_token(), msg)
        elsif !return_expression.nil? && function_return_type.nil?
            msg = "Type error: function expected to return nothing, but return value found to be of type #{expression_type.getType().downcase()}"
            make_and_send_error(expression_type, msg)
        elsif !return_expression.nil? && !function_return_type.nil?
            exp_type = @main_analyzer.getExpressionTypeToken()
            if exp_type.nil?()
                return
            elsif exp_type.getType().downcase() != function_return_type.getType().downcase()
                exp_type_text = exp_type.getType().downcase()
                return_type_text = function_return_type.getType().downcase()
                msg = "Type error: function expected to return #{return_type_text}, but return type found to be #{exp_type_text}"
                make_and_send_error(exp_type, msg)
            end
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
