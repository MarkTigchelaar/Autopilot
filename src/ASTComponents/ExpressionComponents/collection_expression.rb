
class CollectionExpression
    def initialize(left_bracket, elements, right_bracket)
        @left_bracket = left_bracket
        @elements = elements
        @right_bracket = right_bracket
        @checked = false
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def _printLiteral(repr_list)
        repr_list.append(@left_bracket)
        i = 0
        l = @elements.length
        for elem in @elements do
            elem._printLiteral(repr_list)
            if(i < l - 1)
                repr_list.append(',')
            end
            i += 1
        end
        repr_list.append(@right_bracket)
    end

    def _printTokType(type_list)
        type_list.append(@left_bracket)
        i = 0
        l = @elements.length
        for elem in @elements do
            elem._printTokType(type_list)
            if(i < l - 1)
                type_list.append(',')
            end
            i += 1
        end
        type_list.append(@right_bracket)
    end

    def toJSON()
        elems = Array.new()
        for exp in @elements
            elems.append(exp.toJSON())
        end
        return {
            "type" => "collection",
            "left_delimiter" => @left_bracket,
            "right_delimiter" => @right_bracket,
            "elements" => elems
        }
    end
end
