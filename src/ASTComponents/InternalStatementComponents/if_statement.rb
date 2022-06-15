
class IfStatement
    def initialize()
        @let = false
        @var = false
        @unwrapped_var = nil
        @option = nil
        @expression_ast = nil
        @statements = nil
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def set_unwrapped_var(opt)
        @unwrapped_var
    end

    def set_option(opt)
        @option
    end

    def is_let()
        @let = true
    end

    def is_var()
        @var = true
    end

    def set_ast(ast)
        @expression_ast = ast
    end

    def get_ast()
        return @expression_ast
    end

    def set_statements(stmts)
        @statements = stmts
    end

    def get_statements()
        return @statements
    end

    def _printTokType(type_list)
        if(@expression_ast != nil)
            @expression_ast._printTokType(type_list)
        end
        if(@var)
            type_list.append(" var")
        elsif(@let)
            type_list.append(" let")
        end
        if(@var or @let)
            type_list.append(" #{@unwrapped_var.getText()}: #{@option.getText()}")
        end

    end

    def _printLiteral()
        if(@expression_ast != nil)
            l = Array.new
            @expression_ast._printLiteral(l)
            return "exp:" + l.join("")
        end
        type = ""
        if(@var)
            type = "var"
        elsif(@let)
            type = "let"
        end
        msg = ""
        if(@var or @let)
            msg = " #{@unwrapped_var.getText()}: #{@option.getText()}"
        end
        return type + msg
    end

    def toJSON()
        assign_type = "var"
        if(@let)
            assign_type = "let"
        end
        uvar = nil
        if(@unwrapped_var != nil)
            uvar = {
                "literal" => @unwrapped_var.getText(),
                "type" => @unwrapped_var.getType(),
                "line_number" => @unwrapped_option.getLine()
            }
        end
        option = nil
        if(@option != nil)
            option = {
                "literal" => @option.getText(),
                "type" => @option.getType(),
                "line_number" => @option.getLine()
            }
        end
        return {
            "type" => "if",
            "assignment_type" => assign_type,
            "unwrapped_option" => uvar,
            "option" => option,
            "expression" => @expression_ast.toJSON(),
            "statememts" => @statements.toJSON()
        }
    end
end