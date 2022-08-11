
class InterfaceStatement
    def initialize(name, functions)
        @name = name
        @functions = functions
        @is_acyclic = false
        @is_public = false
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def toJSON()
        return {
            "type" => "interface",
            "name" => {
                "literal" => @name.getText(),
                "type" => @name.getType(),
                "line_number" => @name.getLine()
            },
            "functions" => getFunctionsJSON(),
            "attributes" => {
                "acyclic" => @is_acyclic,
                "public" => @is_public
            }
        }
    end

    def getFunctionsJSON()
        funcs = Array.new()
        for fn in @functions
            funcs.append(fn.toJSON())
        end
        return funcs
    end

    def setAsAcyclic()
        @is_acyclic = true
    end

    def setAsPublic()
        @is_public = true
    end

    def _printTokType(type_list)
        if(@is_acyclic)
            type_list.append(ACYCLIC)
        end
        if(@is_public)
            type_list.append(PUB)
        end
        type_list.append(@name.getType())
        for func in @functions
            func._printTokType(type_list)
        end
    end

    def _printLiteral()
        astString = ""
        if(@is_acyclic)
            astString += "acyclic "
        end
        if(@is_public)
            astString += "pub "
        end
        astString += @name.getText() + " "
        for func in @functions
            astString += func._printLiteral() + " "
        end
        astString = astString.strip()
        astString = astString.squeeze(" ")
        return astString
    end
end
