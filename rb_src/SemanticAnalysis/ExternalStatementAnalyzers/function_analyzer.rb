class FunctionAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        stmts = ast_node.get_statements()
        return_type_token = ast_node.get_return_type()
        @main_analyzer.set_return_type(return_type_token)
        @main_analyzer.analyze_node_locally(stmts)
        analyze_args(ast_node.get_args())
        if !return_type_token.nil?
            if found_missing_return_paths(stmts)
                msg = "Function not valid, function returns a value, but not all code paths return a value"
                make_and_send_error(ast_node.get_name(), msg)
            end
        end
    end

    def analyze_args(args) 
        for i in 0 .. args.length - 1 do
            for j in i .. args.length - 1 do
                if i == j
                    next
                end
                if args[i].get_name().getText() == args[j].get_name().getText()
                    msg = "Name Collision, arguments have same name"
                    make_and_send_error(args[i].get_name(), msg)
                end
            end
        end
    end

    # If not a return, then ALL sub statements need a return in them ex:
    # if ... do
    #    ...
    #    return
    # else
    #    ...
    #    return
    # end
    def found_missing_return_paths(statement_list)
        return true if statement_list.nil?
        stmts = statement_list.get_statements()
        return true if stmts.nil?

        last_statement = stmts[stmts.length - 1]
        len = stmts.length
        if ["IfStatement", "ElifStatement", "UnlessStatement", "ForStatement", "LoopStatement", "WhileStatement"].include?(last_statement.class.name)
            return true
        elsif last_statement.class.name != "ReturnStatement" and len > 1
            return_count = 0
            for i in 0 .. len - 1 do
                sub_statements_list = stmts[i].get_statements()
                if sub_statements_list.nil?
                    # no penalty for being a assign or reassign statement
                    return_count += 1
                    next
                end
                unless found_missing_return_paths(sub_statements_list)
                    return_count += 1
                end
            end
            return return_count != len
        end
        return last_statement.class.name != "ReturnStatement"
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
