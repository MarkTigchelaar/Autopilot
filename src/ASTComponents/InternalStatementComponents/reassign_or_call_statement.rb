
class ReassignmentOrCallStatement
    def initialize(var_name, assignment_type_token, expression_ast, functions)
        @var_name = var_name
        @expression_ast = expression_ast
        @functions = functions
        @assignment_type_token = assignment_type_token
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        funcs = Array.new()
        if(@functions != nil)
            for func in @functions
                funcs.append(func.toJSON())
            end
        end
        return {
            "type" => "reassign_or_call",
            "token" => {
                "literal" => getVarNameText(),
                "type" => getVarNameType(),
                "line_number" => getVarNameLine()
            },
            "assignment_type_token" => {
                "literal" => getAssignTypeText(),
                "type" => getAssignType(),
                "line_number" => getLineNumber()
            },
            "functions" => funcs,
            "rvalue" => @expression_ast != nil ? @expression_ast.toJSON() : nil
        }
    end

    

    def getVarNameText()
        name = ""
        name = @var_name.getText() if @var_name
        return name
    end

    def getVarNameType()
        type = ""
        type = @var_name.getType() if @var_name
        return type
    end

    def getVarNameLine()
        line = ""
        line = @var_name.getLine() if @var_name
        return line
    end

    def getAssignTypeText()
        text = ""
        text = @assignment_type_token.getText() if @assignment_type_token
        return text
    end

    def getAssignType()
        type = ""
        type = @assignment_type_token.getType() if @assignment_type_token
        return type
    end

    def getLineNumber()
        line = ""
        line = @assignment_type_token.getLine() if @assignment_type_token
        return line
    end

    def _printTokType(type_list)
        if(@var_name != nil)
            type_list.append(@var_name.getType())
        else
            type_list.append("NONE")
        end
        
        if(@expression_ast != nil)
            type_list.append("|")
            @expression_ast._printTokType(type_list)
        end
        for func in @functions
            type_list.append("|")
            func._printTokType(type_list)
        end
    end

    def _printLiteral()
        if(@functions.length() > 0 and @expression_ast != nil)
            raise Exception.new("can be reassign and call tpye statement.")
        end
        f = Array.new
        str = Array.new
        for func in @functions
            f = Array.new
            func._printLiteral(f)
            for s in f
                str.append(s + "|")
            end
        end
        str = str.join("")

        l = Array.new
        str2 = ""
        if(@expression_ast != nil)
            @expression_ast._printLiteral(l)
        end
        for s in l
            str2 += s + "|"
        end
        var_name = if @var_name then @var_name.getText() else "NONAME" end
        return "|name:#{var_name}|#{str}#{str2}"
    end
end
