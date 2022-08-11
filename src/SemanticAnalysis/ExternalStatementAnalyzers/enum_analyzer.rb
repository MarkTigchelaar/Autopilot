
class EnumAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(enum_ast_node)
        check_fields(enum_ast_node)
        @main_analyzer.register_name(enum_ast_node.get_name(), "enum")
    end

    def check_fields(enum_ast_node)
        fields = enum_ast_node.get_items()
        if fields.nil?
            raise Exception.new("Items are nil, they should not be")
        end
        check_if_enum_is_allowed_enum_type(enum_ast_node)
        # Brute force, but who cares?
        # Later me, that's who
        for i in (0 .. fields.length - 1) do
            for j in (0 .. fields.length - 1) do
                if i == j
                    next
                elsif j < i
                    next
                end
                check_fields_for_duplicate_names(fields[i], fields[j])
                check_fields_for_duplicate_values(fields[i], fields[j])
                # Means the enum doesn't have a type, like enum thingy(int) ...
                if enum_ast_node.get_type().nil? || enum_ast_node.get_type().nil?
                  check_fields_for_mismatched_types(fields[i], fields[j])
                end
            end
            check_field_if_type_matches_enum(fields[i], enum_ast_node.get_type())
            # enums must have names
            check_field_if_name_matches_enum(fields[i], enum_ast_node.get_name())
            check_if_field_is_allowed_enum_type(fields[i])
        end
    end

    def check_fields_for_duplicate_names(field_one, field_two)
        if field_one.getName() == field_two.getName()
            msg = "Duplicate enum field name"
            make_and_send_error(field_two, msg)
        end
    end

    def check_fields_for_duplicate_values(field_one, field_two)
        return if field_one.getDefaultValue() == "null"
        return if field_two.getDefaultValue() == "null"
        if field_one.getDefaultValue() == field_two.getDefaultValue()
            msg = "Duplicate enum value"
            make_and_send_error(field_two, msg)
        end
    end

    def check_fields_for_mismatched_types(field_one, field_two)
        type1 = field_one.getDefaultValueType()
        type2 = field_two.getDefaultValueType()
        if type1 == "NULL" || type2 == "NULL"
            return
        end
        if type1 != type2 && (not_boolean(type1) && not_boolean(type2))
            msg = "Type error, field has mismatched type"
            make_and_send_error(field_two, msg)
        end
    end

    def check_field_if_name_matches_enum(field_one, enum_name)
        if field_one.getName() == enum_name.getText()
            msg = "Name collision, enum field name matches enum name"
            make_and_send_error(field_one, msg)
        end
    end

    def check_field_if_type_matches_enum(field_one, enum_type)
        return if enum_type.nil?
        return if field_one.getDefaultValueType() == "NULL"
        return if field_one.getDefaultValueType() == IDENTIFIER
        if !not_boolean(field_one.getDefaultValueType()) && !not_boolean(enum_type.getType())
            return
        elsif field_one.getDefaultValueType() != enum_type.getType()
            msg = "Type error, enum field type does not match enum type"
            make_and_send_error(field_one, msg)
        end
    end

    def check_if_field_is_allowed_enum_type(field)
        if field.getDefaultValueType() == IDENTIFIER
            msg = "Type error, enum field type cannot be a user defined type \"#{field.getDefaultValue()}\""
            make_and_send_error(field, msg)
        end
    end

    def check_if_enum_is_allowed_enum_type(enum_ast_node)
        # NOTE: the analyzer doesn't even have to care if that type is defined or not,
        # I made the decision that enums should only by primitive types.
        if enum_ast_node.get_types_type() == IDENTIFIER
            msg = "Type error, enum type cannot be a user defined type \"#{enum_ast_node.get_type_literal()}\""
            make_and_send_error_for_enum(enum_ast_node, msg)
        end
    end

    def make_and_send_error_for_enum(enum_ast_node, message)
        err = Hash.new()
        err["file"] = enum_ast_node.get_filename()
        err["tokenLiteral"] = enum_ast_node.get_type_literal()
        err["lineNumber"] = enum_ast_node.get_type_line_number()
        err["message"] = message
        @main_analyzer.add_semantic_error(err)
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

def not_boolean(some_type)
    if some_type != TRUE && some_type != FALSE && some_type != BOOL
        return true
    end
    return false
end