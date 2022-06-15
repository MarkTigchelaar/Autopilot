
class ContinueStatement
    def initialize(token)
        @information = token
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def _printLiteral
        return @information.getText()
    end

    def _printTokType(type_list)
        type_list.append(@information.getType())
    end

    def toJSON()
        return {
            "type" => "continue",
            "line_number" => @information.getLine()
        }
    end
end
