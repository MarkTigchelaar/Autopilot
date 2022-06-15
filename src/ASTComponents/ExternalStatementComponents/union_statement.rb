
class UnionStatement
    def initialize(name, itemList)
        @union_name = name
        @items = itemList
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        return {
            "type" => "union",
            "name" => {
                "literal" => @union_name.getText(),
                "type" => @union_name.getType(),
                "line_number" => @union_name.getLine()
            },
            "itmes" => getItems()
        }
    end

    def getItems()
        items = Array.new()
        for i in @items
            items.append(i.toJSON())
        end
        return items
    end

    def _printLiteral()
        astString = ""
        astString += @union_name.getText() + " "
        for item in @items do
            astString += item.getText() + " "
        end
        return astString.squeeze(' ').rstrip()
    end

    def _printTokType(type_list)
        type_list.append(@union_name.getType())
        for item in @items
            type_list.append(item.getNamesType())
            type_list.append(item.getType())
        end
    end
end


class UnionItemListType
    def initialize(item_name, item_type)
        @item_name = item_name
        @item_type = item_type
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        return {
            "name" => {
                "literal" => @item_name.getText(),
                "type" => @item_name.getType()
            },
            "item_type" => {
                "literal" => @item_type.getText(),
                "type" => @item_type.getType()
            }
        }
    end

    def getText()
        return @item_name.getText() + ' ' + @item_type.getText() + ' '
    end

    def getType()
        return @item_type.getType()
    end

    def getNamesType()
        return @item_name.getType()
    end
end
