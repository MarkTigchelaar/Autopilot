
class DefineStatement
    def initialize( newName, explicitTypeDef)
        #@oldItemComponent = oldItemComponent
        @newNameToken = newName
        @explicitTypeDef = explicitTypeDef
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def get_old_type()
        #@oldItemComponent
        @explicitTypeDef.oldItemComponent()
    end

    def get_new_name_token()
        @newNameToken
    end

    def toJSON()
        return {
            "type" => "define",
            "old_def" => @explicitTypeDef.toJSON(),
            "new_name" => {
                "literal" => @newNameToken.getText(),
                "type" => @newNameToken.getType(),
                "line_number" => @newNameToken.getLine()
            }
        }
    end



    def _printLiteral
        old = @explicitTypeDef._printLiteral()#oldItemComponent().getText()
        _new = @newNameToken.getText()
        return "old def: #{old} new def: #{_new}"
    end

    def _printTokType(item_list)
        @explicitTypeDef._printTokType(item_list)
        item_list.append(@newNameToken.getType())
    end
end
