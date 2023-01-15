
class BreakStatement
    def initialize(loop_label, token)
        @loop_label = loop_label
        @information = token
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def get_loop_label()
        @loop_label
    end

    def get_info()
        @information
    end

    def get_statements()
        nil
    end

    def _printLiteral
        if(@loop_label != nil)
            return @loop_label.getText() + ", " + @information.getText()
        end
        return @information.getText()
    end

    def _printTokType(type_list)
        if(@loop_label != nil)
            type_list.append(@loop_label.getType())
        end
        type_list.append(@information.getType())
    end

    def toJSON()
        return {
            "type" => "break",
            "loop_label" => {
                "literal" => @information.getText(),
                "type" => @information.getType(),
                "line_number" => @information.getLine()
            }
        }
    end
end
