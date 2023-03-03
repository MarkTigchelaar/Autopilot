class ErrorAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        check_fields(ast_node)
    end

    def check_fields(error_ast_node)
        name = error_ast_node.get_name()
        fields = error_ast_node.get_items()
        if fields.nil?
            raise Exception.new("Internal Error: Items are nil, they should not be")
        end
        for i in (0 .. fields.length - 1) do
            for j in (0 .. fields.length - 1) do
                if i == j
                    next
                elsif j < i
                    next
                end
                check_fields_for_duplicate_names(fields[i], fields[j])
            end
            check_field_name_matches_error(fields[i], name)
        end
    end

    def check_fields_for_duplicate_names(field_one, field_two)
        if field_one.getText() == field_two.getText()
            msg = "Duplicate error field name"
            make_and_send_error(field_two, msg)
        end
    end

    def check_field_name_matches_error(field, error_name)
        if field.getText() == error_name.getText()
            msg = "Name collision, error field matches error name"
            make_and_send_error(field, msg)
        end
    end

    def make_and_send_error(field_one, message)
        err = Hash.new()
        err["file"] = field_one.getFilename()
        err["tokenLiteral"] = field_one.getText()
        err["lineNumber"] = field_one.getLine()
        err["message"] = message
        @main_analyzer.add_semantic_error(err)
    end
end
