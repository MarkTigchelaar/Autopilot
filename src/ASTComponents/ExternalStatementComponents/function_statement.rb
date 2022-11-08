
class FunctionStatement
    def initialize(function_name, arguments, return_type, statements)
        @function_name = function_name
        @arguments = arguments
        @return_type = return_type
        @statements = statements
        @is_acyclic = false
        @is_public = false
        @is_inline = false
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def get_name()
        @function_name
    end

    def get_args()
        @arguments
    end

    def get_statements()
        @statements
    end

    def toJSON()
        ret = nil
        if(@return_type != nil)
            ret = {
                "literal" => @return_type.getText(),
                "type" => @return_type.getType(),
                "line_number" => @return_type.getLine()
            }
        end
        return {
            "type" => "function",
            "name" => {
                "literal" => @function_name.getText(),
                "type" => @function_name.getType(),
                "line_number" => @function_name.getLine()
            },
            "arguments" => getArgumentsJSON(),
            "return_type" => ret,
            "attributes" => {
                "acyclic" => @is_acyclic,
                "public" => @is_public,
                "inline" => @is_inline
            },
            "statements" => getStatementsJSON()
        }
    end

    def getArgumentsJSON()
        argsJSON = Array.new()
        for arg in @arguments
            argsJSON.append(arg.toJSON())
        end
        return argsJSON
    end

    def getStatementsJSON()
        stmts = ""
        stmts = @statements.toJSON() if @statements
        return stmts
    end

    def setAsAcyclic()
        @is_acyclic = true
    end

    def setAsPublic()
        @is_public = true
    end

    def setAsInline()
        @is_inline = true
    end

    def _printTokType(type_list)
        if(@is_acyclic)
            type_list.append(ACYCLIC)
        end
        if(@is_inline)
            type_list.append(INLINE)
        end
        if(@is_public)
            type_list.append(PUB)
        end
        type_list.append(@function_name.getType())
        for arg in @arguments
            arg._printTokType(type_list)
        end
        if(@return_type != nil)
            type_list.append(@return_type.getType())
        end
        if(@statements != nil)
            @statements._printTokType(type_list)
        end
    end

    def _printLiteral()
        astString = ""
        if(@is_acyclic)
            astString += "acyclic "
        end
        if(@is_inline)
            astString += "inline "
        end
        if(@is_public)
            astString += "pub "
        end
        astString += @function_name.getText() + " "
        for arg in @arguments
            astString += arg._printLiteral() + " "
        end
        if(@return_type != nil)
            astString += " " + @return_type.getText() + " "
        end
        if(@statements != nil)
            astString += @statements._printLiteral() + " "
        end
        astString = astString.strip()
        astString = astString.squeeze(" ")
        return astString
    end
end


class FunctionArgument
    def initialize(var_name, var_type, default_value = nil)
        @var_name = var_name
        @var_type = var_type
        @default_value = default_value
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def get_name()
        @var_name
    end

    def toJSON()
        default = nil
        if(@default_value != nil)
            default = {
                "literal" => @default_value.getText(),
                "type" => @default_value.getType()
            }
        end
        return {
            "name" => {
                "literal" => @var_name.getText(),
                "type" => @var_name.getType(),
                "line_number" => @var_name.getLine()
            },
            "type" => {
                "literal" => @var_type.getText(),
                "type" => @var_type.getType(),
                "line_number" => @var_type.getLine()
            },
            "default_value" => default
        }
    end

    def _printLiteral()
        str =  @var_name.getText() + " " + @var_type.getText()
        if(@default_value != nil)
            return str + " " + @default_value.getText()
        end
        return str
    end

    def _printTokType(type_list)
        type_list.append(@var_name.getType())
        type_list.append(@var_type.getType())
        if(@default_value != nil)
            type_list.append(@default_value.getType())
        end
    end
end
