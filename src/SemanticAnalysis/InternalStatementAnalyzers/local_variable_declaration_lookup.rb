
# Checks that variables which are being used are :
# 1. Declared previously
# 2. Are same type, or need to be cataloged
# 3. Do not collide with previously defined variables
class LocalVariableDeclarationLookup
    def initialize(analyzer)
        @main_analyzer = analyzer
        @scope_level = 0
        @variable_trackers = Array.new()
    end

    def reset()
        @scope_level = 0
        @variable_trackers = Array.new()
    end

    def inc_scope()
        @scope_level += 1
    end

    def dec_scope()
        @scope_level -= 1
        if(@scope_level < 0)
            raise Exception.new("Scope level below 0")
        end
        forget_deeper_scoped_variables()
    end

    def declare_variable(token, access_modifier, type)
        if(is_defined_in_current_scope(token))
            msg = "Name collision, variable declaration matches previous variable declaration"
            make_and_send_error(token, msg)
            return
        end
        var = LocalVariableTracker.new(token, access_modifier, type, @scope_level)
        @variable_trackers.append(var)
    end

    def is_defined_in_current_scope(token)
        for i in (0 .. @variable_trackers.length - 1) do
            if(@variable_trackers[i].recognizes_token(token))
                return true
            end
        end
        return false
    end

    def is_same_type_as_defined_variable(token)
        for i in (0 .. @variable_trackers.length - 1) do
            if(@variable_trackers[i].recognized_token_is_same_type(token))
                return true
            end
        end
        return false
    end

    def forget_deeper_scoped_variables()
        for i in (0 .. @variable_trackers.length - 1).reverse() do
            if(@variable_trackers[i].is_deeper_scope(@scope_level))
                @variable_trackers.delete_at(i)
            end
        end
    end

    def make_and_send_error(field, message)
        err = Hash.new()
        err["file"] = field.getFilename()
        err["tokenLiteral"] = field.getName()
        err["lineNumber"] = field.getLine()
        err["message"] = message
        @main_analyzer.add_semantic_error(err)
    end
end

class LocalVariableTracker
    def initialize(variable_token, access_modifier, type, scope_level)
        @token = variable_token
        @access_modifier = access_modifier
        @type = type
        @scope_level = scope_level
    end

    def recognizes_token(other_token)
        if(@token.getText() == other_token.getText())
            return true
        end
        return false
    end

    def recognized_token_is_same_type(other_token, type)
        if(recognizes_token(other_token))
            if(@type == type)
                return true
            end
        end
        return false
    end

    def is_deeper_scope(current_scope_level)
        return current_scope_level < @scope_level
    end
end
