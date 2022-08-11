
class StatementList
    def initialize(statements)
        @statements = statements
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def length()
        return @statements.length()
    end

    def toJSON()
        stmts = Array.new()
        for s in @statements
            stmts.append(s.toJSON())
        end
        return stmts
    end

    def _printLiteral
        lit = ""
        for stmt in @statements
            lit += stmt._printLiteral()
        end
        return lit
    end

    def _printTokType(type_list)
        for stmt in @statements
            stmt._printTokType(type_list)
        end
    end
end
