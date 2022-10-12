class NameExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        name = ast_node.getName()
        #@main_analyzer.check_if_external_identifier(name)
        #unless @main_analyzer.variable_is_defined_in_current_scope(name)
        #    msg = "Identifier is not defined."
        #    make_and_send_error(name, msg)
        #end
        if name.getType() == IDENTIFIER
            raise Exception.new("Only constants are implemented currently")
        end
        @main_analyzer.setExpressionTypeToken(name)
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
