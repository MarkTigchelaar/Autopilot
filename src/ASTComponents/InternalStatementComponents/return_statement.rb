
class ReturnStatement
    def initialize(return_expression)
        @return_expression = return_expression
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def toJSON()
        return {
            "type" => "return",
            "rvalue" => @return_expression != nil ? @return_expression.toJSON() : nil,
        }
    end

    def _printLiteral()
        a = Array.new
        @return_expression._printLiteral(a)
        return a.join("")
    end

    def _printTokType(type_list)
        @return_expression._printTokType(type_list)
    end
end
