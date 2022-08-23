class UnionAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(union_ast_node)
        check_fields(union_ast_node)
        #@main_analyzer.register_name(union_ast_node.get_name(), "union")
    end
    
    def check_fields(union_ast_node)
        fields = union_ast_node.get_items()
        if fields.nil?
            raise Exception.new("Items are nil, they should not be")
        end
        for i in (0 .. fields.length - 1) do
            for j in (0 .. fields.length - 1) do
                if i == j
                    next
                elsif j < i
                    next
                end
                check_fields_for_duplicate_names(fields[i], fields[j])
                check_fields_for_duplicate_types(fields[i], fields[j])
            end
            check_field_if_name_matches_union(fields[i], union_ast_node.get_name())
        end
    end

    def check_fields_for_duplicate_names(field_one, field_two)
        if field_one.getName() == field_two.getName()
            msg = "Duplicate union field name"
            make_and_send_error(field_two, msg)
        end
    end

    def check_fields_for_duplicate_types(field_one, field_two)
        if field_one.getTypeLiteral() == field_two.getTypeLiteral()
            msg = "Duplicate union field type \"#{field_one.getTypeLiteral()}\""
            make_and_send_error(field_two, msg)
        end
    end

    def check_field_if_name_matches_union(field_one, union_name)
        if field_one.getName() == union_name.getText()
            msg = "Name collision, union field name matches union name"
            make_and_send_error(field_one, msg)
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

=begin 
[
    {
        "file" : "../Testfiles/SemanticAnalyzerTests/UnionTests/test1.ap",
        "tokenLiteral" : "",
        "lineNumber" : "",
        "message" : ""
    }
] 
=end