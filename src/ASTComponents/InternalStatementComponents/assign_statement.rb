

class AssignmentStatement
    def initialize(let_or_var, name, type, expression_ast)
        @name = name
        @type = type
        @expression_ast = expression_ast
        @let_or_var = let_or_var
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def toJSON()
        return {
            "type" => "assignment",
            "token" => {
                "literal" => @name.getText(),
                "type" => @name.getType(),
                "line_number" => @name.getLine()
            },
            "variable_type" => getType(),
            "assignment_type" => @let_or_var.getType(),
            "rvalue" => @expression_ast.toJSON()
        }
    end

    def getType()
        if(@type)
            return {
                "literal" => @type.getText(),
                "type" => @type.getType(),
                "line_number" => @type.getLine()
            }
        else
            return nil
        end
    end

    def usesLet
        @let = true
    end

    def usesVar
        @var = true
    end

    def _printLiteral
        ownership_type = @let_or_var.getText()
        if(@expression_ast != nil)
            l = Array.new
            @expression_ast._printLiteral(l)
            if(@type != nil)
                t = @type.getText()
            else
                t = ""
            end
            return "name: #{@name.getText()}, type: #{t}, ownership type: #{ownership_type}, exp: " + l.join("")
        else
            raise Exception.new("Expression not found.")
        end
    end

    def _printTokType(type_list)
        type_list.append(@name.getType())
        if(@type != nil)
            type_list.append(@type.getType())
        end
        if(@expression_ast != nil)
            @expression_ast._printTokType(type_list)
        else
            raise Exception.new("Expression not found.")
        end
    end
end