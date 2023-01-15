
class ModuleStatement
    def initialize(moduleinfo)
        @moduleinfo = moduleinfo
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def getName()
        @moduleinfo
    end

    def toJSON()
        return {
            "type" => "module",
            "name" => {
                "literal" => @moduleinfo.getText(),
                "type" => @moduleinfo.getType(),
                "line_number" => @moduleinfo.getLine()
            }
        }
    end

    def _printLiteral
        return @moduleinfo.getText()
    end

    def _printTokType(item_list)
        item_list.append(@moduleinfo.getType())
    end
end
