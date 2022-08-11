
class MethodCallExpression
    def initialize(struct_name_token, methods)
        @struct_name = struct_name_token
        @methods = methods
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def toJSON()
        jsonArgs = Array.new()
        for arg in @args
            jsonArgs.append(arg.toJSON())
        end
        return {
            "type" => "method_call",
            "struct" => @struct_name.toJSON(),
            "methods" => jsonArgs
        }
    end

    def _printLiteral(repr_list)
        @struct_name._printLiteral(repr_list)
        repr_list.append('(')
        i = 0
        l = @methods.length
        for meth in @methods do
            meth._printLiteral(repr_list)
            if(i < l - 1)
                repr_list.append(',')
            end
            i += 1
        end
        repr_list.append(')')
    end

    def _printTokType(type_list)
        @struct_name._printTokType(type_list)
        type_list.append('(')
        i = 0
        l = @methods.length
        for meth in @methods do
            meth._printTokType(type_list)
            if(i < l - 1)
                type_list.append(',')
            end
            i += 1
        end
        type_list.append(')')
    end
end
