
class OperatorExpresison
    def initialize(token, lhs_exp, token_type, rhs_exp)
        @lhs = lhs_exp
        @rhs = rhs_exp
        @type = token_type
        @token = token
        @checked = false
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def _printLiteral(repr_list)
        repr_list.append('(')
        @lhs._printLiteral(repr_list)
        repr_list.append(' ' + @token.getText() + ' ')
        @rhs._printLiteral(repr_list)
        repr_list.append(')')
    end

    def _printTokType(type_list)
        type_list.append('(')
        @lhs._printTokType(type_list)
        type_list.append(' ' + @type.to_s + ' ')
        @rhs._printTokType(type_list)
        type_list.append(')')
    end

    def toJSON()
        return {
            "type" => "binary",
            "token" => {
                "literal" => @token.getText(),
                "type" => @token.getType(),
                "line_number" => @token.getLine()
            },
            "lhs_exp" => @lhs.toJSON(),
            "rhs_exp" => @rhs.toJSON()
        }
    end
end
