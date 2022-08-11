
class ElseStatement
    def initialize(sub_statements)
        @sub_statements = sub_statements
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def _printLiteral
        return "else"
    end

    def _printTokType(type_list)
        type_list.append("ELSE")
    end

    def toJSON()
        return {
            "type" => "else",
            "statememts" => @sub_statements.toJSON()
        }
    end
end