class ImportAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        check_fields(ast_node)
        #@main_analyzer.register_name(ast_node.get_module_name(), "import")
    end

    def check_fields(ast_node)
        items = ast_node.get_item_list()
        for i in (0 .. items.length - 1) do
            for j in (0 .. items.length - 1) do
                if i == j
                    next
                elsif j < i
                    next
                end
                if items[i].getText() == items[j].getText()
                    msg = "Duplicate import field name"
                    make_and_send_error(items[i], msg)
                end
            end
        end
    end

    def make_and_send_error(item, message)
        err = Hash.new()
        err["file"] = item.getFilename()
        err["tokenLiteral"] = item.getText()
        err["lineNumber"] = item.getLine()
        err["message"] = message
        @main_analyzer.add_semantic_error(err)
    end
end
