class StatementListAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        check_order_of_statements(ast_node)
        #check_statement_labels(ast_node)
        for statement in ast_node.get_statements() do
            @main_analyzer.analyze_node_locally(statement)
        end
    end

    def check_order_of_statements(ast_node)
        statements = ast_node.get_statements()
        number_of_statements = statements.length
        for i in 0 .. number_of_statements - 1 do
            stmt = statements[i]
            #name = stmt.get_name() <- fix all statements so they keep their token, for location info.
            case stmt.class.name
            when "ReturnStatement"
                unless i == number_of_statements - 1
                    msg = "Error, return statements cannot be the last statement in a scope"
                    make_and_send_error(name, msg)
                end
            when "BreakStatement"
                unless @main_analyzer.is_inside_loop()
                    msg = "Error, break statements must be inside of a loop"
                    make_and_send_error(name, msg)
                end
            when "ContinueStatement"
                unless @main_analyzer.is_inside_loop()
                    msg = "Error, continue statements must be inside of a loop"
                    make_and_send_error(name, msg)
                end
            when "ElifStatement"
                unless i > 0 && ["IfStatement", "ElifStatement"].include?(statements[i - 1].class.name)
                    msg = "Error, elif statements must be preceded by an if statement, or another elif statement"
                    make_and_send_error(name, msg)
                end
            when "ElseStatement"
                unless i > 0 && ["IfStatement", "ElifStatement"].include?(statements[i - 1].class.name)
                    msg = "Error, else statements must be preceded by an if statement, or an elif statement"
                    make_and_send_error(name, msg)
                end
            else
                next
                #raise Exception.new("Internal error, statement type #{stmt.class.name} not recognized")
            end
        end
    end

    def check_statement_labels(ast_node)
        labels = Array.new()
        for statement in ast_node.get_statements() do
            location_info = statement.get_info()
            case statement.class.name
            when "BreakStatement"
                unless statement.get_loop_label().nil?
                    unless labels.include?(statement.get_loop_label())
                        msg = "Error, break statement label not defined"
                        make_and_send_error(location_info, msg)
                    end
                end
            when "LoopStatement", "ForStatement", "WhileStatement"
                unless statement.get_name().nil?
                    if labels.include?(statement.get_name())
                        msg = "Name collision, loop label is already defined"
                        make_and_send_error(location_info, msg)
                    else
                        labels.append(statement.get_name())
                    end
                end
            end
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
