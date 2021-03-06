
class CallExpression
    def initialize(token, expression, arguments)
        @function = expression
        @args = arguments
        @token = token
        @checked = false
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        jsonArgs = Array.new()
        for arg in @args
            jsonArgs.append(arg.toJSON())
        end
        return {
            "type" => "function_call",
            "name" => {
                "literal" => @token.getText(),
                "type" => @token.getType(),
                "line_number" => @token.getLine()
            },
            "lhs_exp" => @function.toJSON(),
            "arguments" => jsonArgs
        }
    end

    def _printLiteral(repr_list)
        @function._printLiteral(repr_list)
        repr_list.append('(')
        i = 0
        l = @args.length
        for arg in @args do
            arg._printLiteral(repr_list)
            if(i < l - 1)
                repr_list.append(',')
            end
            i += 1
        end
        repr_list.append(')')
    end

    def _printTokType(type_list)
        @function._printTokType(type_list)
        type_list.append('(')
        i = 0
        l = @args.length
        for arg in @args do
            arg._printTokType(type_list)
            if(i < l - 1)
                type_list.append(',')
            end
            i += 1
        end
        type_list.append(')')
    end
end