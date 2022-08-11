
class ElifStatement
    def initialize(if_statement)
        @if_statement = if_statement
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def toJSON()
        json = @if_statement.toJSON()
        json["type"] = "elif"
        return json
    end

    def _printLiteral
        if(@if_statement != nil)
            return @if_statement._printLiteral()
        end
        return ""
    end

    def _printTokType(type_list)
        if(@if_statement != nil)
            @if_statement._printTokType(type_list)
        end
    end
end
