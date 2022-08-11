
class EnumStatement
    def initialize(name, itemList, generaltype)
        @name = name
        @items = itemList
        @enumtype = generaltype
    end

    def visit(semantic_analyzer)
        # lets semantic analyzer figure out which analyzer to use
        semantic_analyzer.analyze_node_locally(self)
    end

    def get_items()
        return @items
    end

    def get_name()
        return @name
    end

    def get_type()
        return @enumtype
    end

    def get_types_type()
        return "NULL" unless @enumtype
        return @enumtype.getType()
    end

    def get_type_literal()
        return "" unless @enumtype
        return @enumtype.getText()
    end

    def get_type_line_number()
        return @enumtype.getLine()
    end

    def get_filename()
        return @enumtype.getFilename()
    end

    def toJSON()
        type_lit = ""
        type_lit = @enumtype.getText() if @enumtype
        type_type = ""
        type_type = @enumtype.getType() if @enumtype
        line = ""
        line = @enumtype.getLine() if @enumtype
        return {
            "type" => "enum",
            "name" => {
                "literal" => @name.getText(),
                "type" => @name.getType(),
                "line_number" => @name.getLine()
            },
            "fields" => getItemsJSON(),
            "enumtype" => {
                "literal" => type_lit,
                "type" => type_type
            }
        }
    end

    def getItemsJSON()
        itemList = Array.new()
        for item in @items
            itemList.append(item.toJSON())
        end
        return itemList
    end

    def _printLiteral()
        ename = "null"
        if @name != nil
            ename = @name.getText()
        end
        enumtype = "null"
        if @enumtype != nil
            enumtype = @enumtype.getText()
        end
        astJSON = "("
        
        astJSON += "name" + " : " + ename + ", "
        astJSON += "type" + " : " + enumtype + ", "
        astJSON += "items" + " : ["
        for item in @items do
            astJSON += printItem(item) + ", "
        end
        astJSON = astJSON[0...-2]
        return astJSON + "])"
    end

    def printItem(item)
        itemString = ""
        itemString += "(name : " + item.getName() + ", "
        itemString += "default_value" + " : " + item.getDefaultValue()
        itemString += ")"
        return itemString
    end

    def _printTokType(item_list)
        item_list.append(@name.getType())
        if(@enumtype != nil)
            item_list.append(@enumtype.getType())
          end
        for item in @items do
            item_list.append(item.getType().upcase)
            item_list.append(item.getDefaultValueType())
        end
    end
end

class EnumListItem
    def initialize(name, default_value_token)
        @name = name
        @default_value_token = default_value_token
    end

    def toJSON()
        default_literal = ""
        default_literal = @default_value_token.getText() if @default_value_token != nil
        default_value = ""
        default_value = @default_value_token.getType() if @default_value_token != nil

        return {
            "name" => {
                "literal" => @name.getText(),
                "type" => @name.getType(),
                "line_number" => @name.getLine()
            },
            "default_value" => {
                "literal" => default_literal,
                "type" => default_value,
                "line_number" => @name.getLine()
            }
        }
    end

    def getFilename()
        return @name.getFilename()
    end

    def getName()
        return @name.getText()
    end

    def getLine()
        return @name.getLine()
    end

    def getType()
        # type of enum, not the type of the token
        if @name != nil
            return @name.getType()
        else
            return "null"
        end
    end

    def getDefaultValue()
        if @default_value_token != nil
            return @default_value_token.getText()
        else
            return "null"
        end
    end

    def getDefaultValueType()
        if @default_value_token != nil
            return @default_value_token.getType()
        else
            return "NULL"
        end
    end
end
