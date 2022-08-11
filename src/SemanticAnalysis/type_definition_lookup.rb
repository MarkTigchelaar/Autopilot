class TypeDefinitionLookup
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
        # for checking for name collisions
        @module_to_name_tokens_map = Hash.new()
        # for type checking
        @mod_to_type_to_name_nested_map = NestedHash.new()
    end

    def reset()
        @module_to_name_tokens_map = Hash.new()
        @mod_to_type_to_name_nested_map = NestedHash.new()
    end

    # Just checks in types for each module, does not deal with name collisions
    # with items being used that are imported from a different module.
    # Will be involved, but the logic will be elsewhere
    def register_name(mod, name_token, construct_type)
        if @module_to_name_tokens_map.has_key?(mod)
            for existing_name in @module_to_name_tokens_map[mod] do
                if name_token.getText() == existing_name.getText()
                    message = new_name_error_message(mod, existing_name, construct_type)
                    make_and_send_error(name_token, message)
                    return
                end
            end
            @module_to_name_tokens_map[mod].append(name_token)
            add_to_mod_type_name_map(mod, name_token, construct_type)
        elsif !mod.nil?
            add_to_module_name_map(mod, name_token)
            add_to_mod_type_name_map(mod, name_token, construct_type)
        else
            raise Exception.new("Internal error, module is nil")
        end
    end

    def add_to_module_name_map(mod, name_token)
        names = Array.new()
        names.append(name_token)
        @module_to_name_tokens_map[mod] = names
    end

    def add_to_mod_type_name_map(mod, name_token, construct_type)
        @mod_to_type_to_name_nested_map.insert(mod, construct_type, name_token)
    end

    def make_and_send_error(field, message)
        err = Hash.new()
        err["file"] = field.getFilename()
        err["tokenLiteral"] = field.getText()
        err["lineNumber"] = field.getLine()
        err["message"] = message
        @main_analyzer.add_semantic_error(err)
    end

    def new_name_error_message(mod, existing_name_token, construct_type)
        unless mod
            mod_dot = ""
        else
            mod_dot = mod + "."
        end
        type = nil
        if @mod_to_type_to_name_nested_map.has_key?(mod)
            type = @mod_to_type_to_name_nested_map.get_type(mod)
        else
            raise Exception.new("Internal error, no type being mapped to from construct name")
        end
        if type != construct_type
            raise Exception.new("Internal error, #{type} != #{construct_type}")
        end
        return "Name collision, #{mod_dot}#{existing_name_token.getText()} of type \"#{construct_type}\" name matches item of same type (#{type})"
    end

    # This is used AFTER first pass of parser / SA of the ENTIRE FILE
    def check_for_definition(type_token)
        return
    end
end





class NestedHash
    def initialize()
        @module_to_types_map = Hash.new()
    end

    def insert(module_name, construct_type, name_token)
        if !@module_to_types_map.has_key?(module_name)
            @module_to_types_map[module_name] = InnerListContainer.new(construct_type)
        end
        @module_to_types_map[module_name].insert(name_token)
    end

    def has_key?(module_name)
        @module_to_types_map.has_key?(module_name)
    end

    def get_type(module_name)
        @module_to_types_map[module_name].get_type()
    end

    def try_get(module_name)
        if @module_to_types_map.has_key?(module_name)
            return @module_to_types_map[module_name].get_names()
        else
            return nil
        end
    end
end

class InnerListContainer
    def initialize(construct_type)
        @names = Array.new()
        @construct_type = construct_type
    end

    def insert(name_token)
        @names.append(name_token)
    end

    def get_type()
        @construct_type
    end

    def get_names()
        return @names
    end
end
