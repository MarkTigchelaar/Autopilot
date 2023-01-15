class ReAssignOrCallAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        name = ast_node.get_name()
        ast = ast_node.get_expressions()
        if !ast.nil?()
            @main_analyzer.analyze_node_locally(ast)
            exp_type_tok = @main_analyzer.getExpressionTypeToken()
            assignment_operator = ast_node.get_assignment_operator()
            if assignment_operator.nil?()
                raise Exception.new("Internal error: assignment operator is missing")
            end
            compatability_list = get_compatability_list_for_combined_assignment(assignment_operator)
            unless compatability_list.include?(exp_type_tok.getType())
                msg = "R value expression is not compatable with assignment operator"
                make_and_send_error(assignment_operator, msg)
            end
            # index = ast_node.get_index_token()
            # checkfor int, long, or a variable
        else
            # array or key index must be considered (add to parser)
            # as well as public fields
            # niether are present in parser
            return
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
