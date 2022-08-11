
class NameExpression
    def initialize(token)
        @token = token
        @checked = false
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def get_name
        return @token.getText()
    end

    def getType
        return @token.getType()
    end

    def _printLiteral(repr_list)
        repr_list.append(get_name())
    end

    def _printTokType(type_list)
        type_list.append(@token.getType())
    end

    def toJSON()
        return {
            "type" => "identifier_or_literal",
            "token" => {
                "literal" => @token.getText(),
                "type" => @token.getType(),
                "line_number" => @token.getLine()
            }
        }
    end
end
