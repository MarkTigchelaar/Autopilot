
class UnlessStatement
    def initialize(if_statement)
        if(if_statement == nil)
            @ast = nil
            @statements = nil
            return
        end
        ast = if_statement.get_ast()
        stmts = if_statement.get_statements()
        @ast = nil
        if(ast != nil)
            @ast = ast
        end
        @statements = nil
        if(ast != nil)
            @statements = stmts
        end
        @if = if_statement
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        json = @if.toJSON()
        json["type"] = "unless"
        return json
    end

    def _printLiteral
        l = Array.new
        if(@ast != nil)
            @ast._printLiteral(l)
        end
        return l.join("")
    end

    def _printTokType(type_list)
        if(@ast != nil)
            @ast._printTokType(type_list)
        end
    end
end
