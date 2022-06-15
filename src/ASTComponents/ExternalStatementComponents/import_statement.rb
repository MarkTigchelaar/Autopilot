
class ImportStatement
    def initialize(modulename, itemList, isLibrary)
        @modulename = modulename
        @itemList = itemList
        @isLibrary = isLibrary
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        return {
            "type" => "module",
            "name" => {
                "literal" => @modulename.getText(),
                "type" => @modulename.getType(),
                "line_number" => @modulename.getLine()
            },
            "import_list" => getImportListJSON(),
            "is_library" => @isLibrary
        }
    end

    def getImportListJSON()
        items = Array.new()
        for item in @itemList
            items.append({
                "literal" => item.getText(),
                "type" => item.getType(),
                "line_number" => item.getLine()
            })
        end
        return items
    end

    def _printLiteral
        libormod = "mod"
        if(@isLibrary)
            libormod = "lib"
        end
        items = ""
        for item in @itemList
            items += item + ","
        end
        if(items[-1] == ',')
            items = items[0 .. -1]
        end
        if(items == "")
            items = "none"
        end
        return "name:#{@modulename.getText()} type:#{libormod} items:[#{items}]"
    end

    def _printTokType(item_list)
        for item in @itemList
            item_list.append(item.getType())
        end
    end
end
