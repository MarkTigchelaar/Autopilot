
class DefineStatement
    def initialize( newName, explicitTypeDef)
        @newNameToken = newName
        @explicitTypeDef = explicitTypeDef
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def get_old_type()
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
        old = @explicitTypeDef._printLiteral()
        _new = @newNameToken.getText()
        return "old def: #{old} new def: #{_new}"
    end

    def _printTokType(item_list)
        @explicitTypeDef._printTokType(item_list)
        item_list.append(@newNameToken.getType())
    end
end

class KeyValueType
    def initialize(tokenTypeToken)
        @tokenTypeToken = tokenTypeToken # several types, which one?
        @key_token = nil
        @value_token = nil
    end

    def add_key_token(key_token)
        @key_token = key_token
    end

    def add_value_token(value_token)
        @value_token = value_token
    end

    def _printLiteral
        @tokenTypeToken.getText() + "(" + @key_token.getText() + ":" + @value_token.getText() + ")"
    end

    def _printTokType(item_list)
        item_list.append(@tokenTypeToken.getType())
        item_list.append(@key_token.getType())
        item_list.append(@value_token.getType())
    end

    def toJSON()

    end
end

class LinearType
    def initialize(tokenTypeToken)
        @tokenTypeToken = tokenTypeToken # several types, which one?
        @value_token = nil
    end

    def add_value_token(value_token)
        @value_token = value_token
    end

    def _printLiteral
        @tokenTypeToken.getText() + "(" + @value_token.getText() + ")"
    end

    def _printTokType(item_list)
        item_list.append(@tokenTypeToken.getType())
        item_list.append(@value_token.getType())
    end

    def toJSON()

    end
end

class RenameType
    def initialize(tokenTypeToken)
        @tokenTypeToken = tokenTypeToken
    end

    def _printLiteral
        @tokenTypeToken.getText()
    end

    def _printTokType(item_list)
        item_list.append(@tokenTypeToken.getType())
    end

    def toJSON()
        {
            "literal" => @tokenTypeToken.getText(),
            "type" => @tokenTypeToken.getType(),
            "line_number" => @tokenTypeToken.getLine()
        }
    end
end

class ResultType
    def initialize(tokenTypeToken)
        @tokenTypeToken = tokenTypeToken # several types, which one?
        @value_token = nil
        @error_type_token = nil
    end

    def add_value_token(value_token)
        @value_token = value_token
    end

    def add_error_type_token(error_type_token)
        @error_type_token = error_type_token
    end

    def _printLiteral
        @tokenTypeToken.getText + "(" + @value_token.getText() + "," + @error_type_token.getText() + ")"
    end

    def _printTokType(item_list)
        item_list.append(@tokenTypeToken.getType())
        item_list.append(@value_token.getType())
        item_list.append(@error_type_token.getType())
    end

    def toJSON()

    end
end

class FunctionType
    def initialize(tokenTypeToken)
        @tokenTypeToken = tokenTypeToken # several types, which one?
        @return_type_token = nil
        @arg_types_list = Array.new()
    end

    def add_arg_type_token(value_token)
        @arg_types_list.append(value_token)
    end

    def add_return_type_token(return_type_token)
        @return_type_token = return_type_token
    end

    def _printLiteral
        args = ""
        @arg_types_list.each do |arg|
            args += arg.getText() + ","
        end
        args = args.delete_suffix(",")
        @tokenTypeToken.getText() + "(" + args + ")" + @return_type_token.getText()
    end

    def _printTokType(item_list)
        item_list.append(@tokenTypeToken.getType())
        @arg_types_list.each do |arg|
            item_list.append(arg.getType())
        end
        item_list.append(@return_type_token.getType())
    end

    def toJSON()

    end
end

class TypeDef
    def initialize()
        @sub_container = nil
    end

    def addSubType(sub_container)
        @sub_container = sub_container
    end

    def addMapValueToken(valueTypeToken)
        @sub_container.add_value_token(valueTypeToken)
    end

    def addMapKeyToken(keyTypeToken)
        @sub_container.add_key_token(keyTypeToken)
    end
    
    def addFunctionReturnTypeToken(funcReturnTypeToken)
        @sub_container.add_return_type_token(funcReturnTypeToken)
    end

    def addFunctionArgToken(funcArgTypeToken)
        @sub_container.add_arg_type_token(funcArgTypeToken)
    end

    def addResultErrorTypeToken(errorTypeToken)
        @sub_container.add_error_type_token(errorTypeToken)
    end

    def addResultTypeToken(resultTypeToken)
        @sub_container.add_value_token(resultTypeToken)
    end

    def addLinearTypeToken(linearTypeToken)
        @sub_container.add_value_token(linearTypeToken)
    end

    def _printLiteral()
        @sub_container._printLiteral()
    end

    def _printTokType(item_list)
        @sub_container._printTokType(item_list)
    end

    def toJSON()
        @sub_container.toJSON()
    end
end