
class ForStatement
    def initialize(loop_name, let, var, var_one, var_two, opt_variable, start_collection_ast, stop_collection_ast, statements)
        @loop_name = loop_name
        @start_collection_ast = start_collection_ast
        @stop_collection_ast = stop_collection_ast
        @statements = statements
        @let = let
        @var = var
        @var_one = var_one
        @var_two = var_two
        @opt_variable = opt_variable
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        json = Hash.new()
        json["type"] = "forloop"
        if(@let)
            json["assignment_type"] = "let"
        elsif(@var)
            json["assignment_type"] = "var"
        end
        if @var_one
            json["variable_one"] = {
                "literal" => @var_one.getText(),
                "type" => @var_one.getType(),
                "line_number" => @var_one.getLine()
            }
        end
        if @var_two
            json["variable_two"] = {
                "literal" => @var_two.getText(),
                "type" => @var_two.getType(),
                "line_number" => @var_two.getLine()
            }
        end
        if @opt_variable
            json["unwrapped_option"] = {
                "literal" => @opt_variable.getText(),
                "type" => @opt_variable.getType(),
                "line_number" => @opt_variable.getLine()
            }
        end
        if @start_collection_ast != nil
            json["start_expression"] = @start_collection_ast.toJSON()
        end
        if @stop_collection_ast != nil
            json["stop_expression"] = @stop_collection_ast.toJSON()
        end
        if(@loop_name != nil)
            json["label"] = {
                "literal" => @loop_name.getText(),
                "type" => @loop_name.getType(),
                "line_number" => @loop_name.getLine()
            }
        end
        if @statements != nil
            json["statements"] = @statements.toJSON()
        end
        return json
    end

    def _printLiteral()
        lit = ""
        if @let
            lit += "let "
        elsif @var
            lit += "var "
        end
        if @var_one
            lit += @var_one.getText() + ' '
        end
        if @var_two
            lit += @var_two.getText() + ' '
        end
        if @opt_variable
            lit += @opt_variable.getText() + ' '
        end
        if @start_collection_ast != nil
            l = Array.new
            ast = @start_collection_ast
            ast._printLiteral(l)
            lit += l.join(" ") + ' '
        end
        if @stop_collection_ast != nil
            l = Array.new
            ast = @stop_collection_ast
            ast._printLiteral(l)
            lit += l.join(" ") + ' '
        end
        if(@loop_name != nil)
            lit += @loop_name.getText() + ' '
        end
        if @statements != nil
            lit += @statements._printLiteral() + ' '
        end
        return lit.strip()
    end

    def _printTokType(type_list)
        if @let
            type_list.append("let")
        elsif @var
            type_list.append("var")
        end
        if @var_one
            type_list.append(@var_one.getType())
        end
        if @var_two
            type_list.append(@var_two.getType())
        end
        if @opt_variable
            type_list.append(@opt_variable.getType())
        end
        if(@loop_name != nil)
            type_list.append(@loop_name.getType())
        end
        if @start_collection_ast != nil
            ast = @start_collection_ast
            ast._printTokType(type_list)
        end
        if @stop_collection_ast != nil
            ast = @stop_collection_ast
            ast._printTokType(type_list)
        end
        if @statements != nil
            @statements._printTokType(type_list)
        end
    end
end