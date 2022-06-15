
class DefineStatement
    def initialize(oldName, newName)
        @oldNameToken = oldName
        @newNameToken = newName
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        return {
            "type" => "define",
            "old_name" => {
                "literal" => @oldNameToken.getText(),
                "type" => @oldNameToken.getType(),
                "line_number" => @oldNameToken.getLine()
            },
            "new_name" => {
                "literal" => @newNameToken.getText(),
                "type" => @newNameToken.getType(),
                "line_number" => @newNameToken.getLine()
            }
        }
    end

    def _printLiteral
        return "old name: #{@oldNameToken.getText()} new name: #{@newNameToken.getText()}"
    end

    def _printTokType(item_list)
        item_list.append(@oldNameToken.getType())
        item_list.append(@newNameToken.getType())
    end
end
