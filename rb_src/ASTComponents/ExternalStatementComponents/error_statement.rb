
class ErrorStatement
    def initialize(name, itemList)
        @name = name
        @items = itemList
    end

    def get_name()
        @name
    end

    def get_items()
        @items
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def toJSON()
        return {
            "type" => "error",
            "name" => {
                "literal" => @name.getText(),
                "type" => @name.getType(),
                "line_number" => @name.getLine()
            },
            "error_list" => getErrorsList()
        }
    end

    def getErrorsList
        errs = Array.new()
        for err in @items
            errs.append({
                "literal" => err.getText(),
                "type" => err.getType(),
                "line_number" => err.getLine()
            })
        end
        return errs
    end

    def _printLiteral()
        astString = ""
        astString += @name.getText() + " "
        for item in @items do
            astString += item.getText() + " "
        end
        
        return astString.rstrip()
    end

    def _printTokType(type_list)
        if(@name != nil)
            type_list.append(@name.getType())
        end
        for item in @items
            type_list.append(item.getType())
        end
    end
end
