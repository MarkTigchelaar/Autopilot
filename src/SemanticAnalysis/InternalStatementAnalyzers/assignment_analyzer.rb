class AssignmentAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    # What is available to this analyzer?
    # local variable lookup
    # arguments sent in (locals again?)
    def analyze_node_locally(ast_node)
        name = ast_node.getName()
        accessor = ast_node.getLetOrVar()
        
        @main_analyzer.analyze_node_locally(ast_node.getExpressionAst())
        type = ast_node.getTypeName()
        exp_type = @main_analyzer.getExpressionTypeToken()
        if type.nil? && exp_type.nil?
            raise Exception.new("Assignment variable type could not be determined")
        elsif type.nil?
            type = exp_type
        elsif type.getText() != exp_type.getText()
            msg = "Expressions value does not resolve to assigned variables type"
            make_and_send_error(type, msg)
        end
        #@main_analyzer.declare_local_variable(name, accessor, type)
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
