require_relative '../../tokentype.rb'


class IfAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        #return
        # just needs to check if expression resolves to a bool
        # aannndd check optional types for name collisions
        # and register optional variable as a let or var variable
        if ast_node.get_unwrapped_var().nil? && ast_node.get_option().nil?
            @main_analyzer.analyze_node_locally(ast_node.get_ast())
            exp_type_tok = @main_analyzer.getExpressionTypeToken()
            if ![BOOL, TRUE, FALSE].include?(exp_type_tok.getType())
                msg = "Expression does not resolve to a bool"
                make_and_send_error(exp_type_tok, msg)
            end
        elsif ast_node.get_unwrapped_var().nil? || ast_node.get_option().nil?
            raise Exception.new("Internal error, optional variable, or unwrapped option not present")
        else
            # has optional type unwrapping
            #return
            variable = ast_node.get_unwrapped_var()
            option = ast_node.get_option()
            if variable.getText() == option.getText()
                msg = "Name Collision, unwrapped option has same name as option"
                make_and_send_error(exp_type_tok, msg)
            end
            # add to resolve database
        end
        @main_analyzer.analyze_node_locally(ast_node.get_statements())
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
