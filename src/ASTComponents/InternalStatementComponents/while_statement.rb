
class WhileStatement
    def initialize(loop_name, expression_ast, statements)
        @loop_name = loop_name
        @expression_ast = expression_ast
        @statements = statements
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def get_name()
        @loop_name
    end

    def get_ast()
        @expression_ast
    end

    def get_statements()
        @statememts
    end

    def toJSON()
        return {
            "name" => get_name(),
            "expression" => @expression_ast.toJSON(),
            "statements" => @statements.toJSON()
        }
    end

    def get_name()
        lit = ""
        lit = @loop_name.getText() if @loop_name
        type = ""
        type = @loop_name.getType() if @loop_name
        line = ""
        line = @loop_name.getLine() if @loop_name
        {
            "literal" => lit,
            "type" => type,
            "line_number" => line
        }
    end

    def _printTokType(type_list)
        if(@loop_name != nil)
            type_list.append(@loop_name.getType())
        end
        if(@expression_ast != nil)
            @expression_ast._printTokType(type_list)
        end
        @statements._printTokType(type_list)
    end

    def _printLiteral()
        l = Array.new
        @expression_ast._printLiteral(l)
        msg = "exp: " + l.join("")
        name = ""
        if(@loop_name != nil)
            name = "name: " + @loop_name.getText() + ", "
        end
        return name + msg
    end
end