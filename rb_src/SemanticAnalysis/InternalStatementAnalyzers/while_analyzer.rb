class WhileLoopAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        puts("analyzing a while")
        @main_analyzer.analyze_node_locally(ast_node.get_ast())
        exp_type_tok = @main_analyzer.getExpressionTypeToken()
        if ![BOOL, TRUE, FALSE].include?(exp_type_tok.getType())
            msg = "expression does not resolve to a bool"
            make_and_send_error(exp_type_tok, msg)
        end
        # name = ast_node.get_name()
        statements = ast_node.get_statements()
        @main_analyzer.analyze_node_locally(statements)
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
