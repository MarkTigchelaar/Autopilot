
class LoopStatement
    def initialize(name, sub_statements)
        @name = name
        @sub_statements = sub_statements
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def get_name()
        @name
    end

    def get_statements()
        @sub_statements
    end

    def toJSON()
        return {
            "type" => "loop",
            "label" =>  @name != nil ? { "literal" => @name.getText(), "type" => @name.getType(), "line_number" => @name.getLine() } : nil,
            "statements" => @sub_statements.toJSON()
        }
    end

    def _printLiteral
        l = Array.new
        if(@name != nil)
            l.append(@name.getText())
        end
        l.append(@sub_statements._printLiteral())
        return l.join("")
    end

    def _printTokType(type_list)
        if(@name != nil)
            type_list.append(@name.getType())
        end
        @sub_statements._printTokType(type_list)
    end
end