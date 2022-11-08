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
        
        expression_ast = ast_node.getExpressionAst()
        @main_analyzer.analyze_node_locally(expression_ast)
        type = ast_node.getTypeName()
        exp_type = @main_analyzer.getExpressionTypeToken()
        if type.nil? && exp_type.nil?
            raise Exception.new("Assignment variable type could not be determined")
        elsif exp_type.getType().nil?
            return # error will have been raised about rvalue being invalid already
        elsif type.nil?
            type = exp_type
        elsif type.getType() != exp_type.getType()
            # ints / floats allowed to be assigned to bigger versions
            # of same type
            unless (type.getType() == LONG && exp_type.getType() == INT) or (type.getType() == DOUBLE && exp_type.getType() == FLOAT)
                msg = "Expressions value: #{exp_type.getText()} of type: \"#{exp_type.getType().downcase()}\" does not resolve to assigned variables type"
                make_and_send_error(type, msg)
            end
        end
        # do something with "type", like register it for later
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
