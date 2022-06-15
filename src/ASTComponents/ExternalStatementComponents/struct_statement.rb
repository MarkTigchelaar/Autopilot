
class StructStatement
    def initialize(name, interfaces, fields, functions)
        @name = name
        @interfaces = interfaces
        @fields = fields
        @functions = functions
        @is_acyclic = false
        @is_public = false
        @is_inline = false
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        return {
            "type" => "struct",
            "name" => {
                "literal" => @name.getText(),
                "type" => @name.getType(),
                "line_number" => @name.getLine()
            },
            "attributes" => {
                "acyclic" => @is_acyclic,
                "public" => @is_public,
                "inline" => @is_inline
            },
            "interfaces" => getInterfacesJSON(),
            "fields" => getFieldsJSON(),
            "functions" => getFunctionsJSON()
        }
    end

    def getInterfacesJSON()
        interfaces = Array.new()
        for i in @interfaces
            interfaces.append({
                "literal" => i.getText(),
                "type" => i.getType(),
                "line_number" => i.getLine()
            })
        end
        return interfaces
    end

    def getFieldsJSON()
        fields = Array.new()
        for f in @fields
            fields.append(f.toJSON())
        end
        return fields
    end

    def getFunctionsJSON()
        fns = Array.new()
        for f in @functions
            fns.append(f.toJSON())
        end
        return fns
    end

    def setAsAcyclic
        @is_acyclic = true
    end

    def setAsPublic
        @is_public = true
    end

    def setAsInline
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
        type_list.append(@name.getType())
        for i in @interfaces
            type_list.append(i.getType())
        end
        for field in @fields
            field._printTokType(type_list)
        end
        for fun in @functions
            fun._printTokType(type_list)
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
        astString += @name.getText() + " "
        for i in @interfaces
            astString += i.getText() + " "
        end
        for field in @fields
            astString += field._printLiteral()
        end
        for fun in @functions
            astString += " " + fun._printLiteral()
        end
        astString = astString.strip()
        astString = astString.squeeze(" ")
        return astString
    end
end


class StructField
    def initialize(name, type, is_public)
        @name = name
        @type = type
        @is_public = is_public
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        return {
            "name" => {
                "literal" => @name.getText(),
                "type" => @name.getType(),
                "line_number" => @name.getLine()
            },
            "type" => {
                "literal" => @type.getText(),
                "type" => @type.getType(),
                "line_number" => @type.getLine()
            },
            "public" => @is_public
        }
    end

    def _printTokType(type_list)
        if(@is_public)
            type_list.append(PUB)
        end
        type_list.append(@name.getType())
        type_list.append(@type.getType())
    end

    def _printLiteral()
        str = ""
        if(@is_public)
            str += "pub "
        end
        str += @name.getText() + " "
        str += @type.getText() + " "
        return str
    end
end
