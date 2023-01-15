class SwitchStatementAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        test_case = ast_node.get_test_case()
        cases = ast_node.get_case_statements()
        default = ast_node.get_default_case()
        seen = Array.new()
        seen.append(test_case.getText())
        for i in 0 .. cases.length - 1 do
            values = cases[i].get_values()
            for value in values do
                if seen.include?(value.getText())
                    msg = "Name collision, value is already defined"
                    make_and_send_error(value, msg)
                end
                if test_case.getType() != value.getType()
                    msg = "Type mismatch, value in switch statement is not the same type as the test case"
                    make_and_send_error(value, msg)
                end
            end
            @main_analyzer.analyze_node_locally(cases[i].get_statements())
        end
        @main_analyzer.analyze_node_locally(default.get_statements())
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
