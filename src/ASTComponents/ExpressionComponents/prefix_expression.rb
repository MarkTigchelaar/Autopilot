
class PreFixExpression
    def initialize(token, operator, right_exp)
        @operator = operator
        @rhs_exp = right_exp
        @token = token
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def getRhsExp()
        @rhs_exp
    end

    def getOperator()
        @operator
    end

    def getName()
        @token
    end

    def _printLiteral(repr_list)
        repr_list.append("(")
        @rhs_exp._printLiteral(repr_list)
        repr_list.append(")")
    end

    def _printTokType(type_list)
        type_list.append("(")
        @rhs_exp._printLiteral(type_list)
        type_list.append(")")
    end

    def toJSON()
        return {
            "type" => "prefix",
            "token" => {
                "literal" => @token.getText(),
                "type" => @token.getType(),
                "line_number" => @token.getLine()
            },
            "rhs_exp" => @rhs_exp.toJSON()
        }
    end
end
