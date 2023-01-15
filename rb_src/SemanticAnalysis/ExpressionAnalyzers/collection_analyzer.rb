class CollectionExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        #return
        # If [] then : can't be included
        # if {} : can, but must be all or nothing (set, or map, but not both)
        # types of each expression cannot be different, they must be the same at each step
        # collections cannot be inside of collection literals, this is a restriction
        # only analyzing constants/literals, since SA does not currently have "memory"
        if ast_node.leftBracket() == "{"
            if ast_node.rightBracket() != "}"
                raise Exception.new("Internal error, closing bracket mismatch")
            end
            analyze_set_or_map(ast_node)
        elsif ast_node.leftBracket() == "["
            if ast_node.rightBracket() != "]"
                raise Exception.new("Internal error, closing bracket mismatch")
            end
            analyze_list(ast_node)
        else
            raise Exception.new("Internal error, no brackets found")
        end
    end

    def analyze_set_or_map(ast_node)
        elements = ast_node.getElements()
        # if COLON type, grab LHS, RHS and analyze
        # match all LHS with all RHS, everything should match
        # later, keep final K,V types to compare against variable literal is assigned to
        colon_count = 0
        for elem in elements do
            # could be name token, prefix, or operator
            exp_name = elem.getName()
            if exp_name.nil? # is a collection!
                msg = "Nested collection literals are illegal!"
                make_and_send_error(ast_node.getName(), msg)
                return
            end
            if exp_name.getType() == COLON
                colon_count += 1
            end
        end
        if colon_count == 0
            # must be a set, but works the same as lists
            analyze_list(ast_node)
        elsif colon_count != elements.length
            first_elem = elements[0]
            msg = "Hash literal has missing key or value"
            make_and_send_error(first_elem.getName(), msg)
            return
        else
            analyze_confirmed_map(ast_node)
        end
    end

    def analyze_list(ast_node)
        elements = ast_node.getElements()
        exp_types = Array.new()
        for elem in elements do
            exp_name = elem.getName()
            if exp_name.nil? # is a collection!
                raise Exception.new("Nested collection literals are illegal!")
            end
            @main_analyzer.analyze_node_locally(elem)
            exp_type = @main_analyzer.getExpressionTypeToken()
            exp_types.append(exp_type)
        end
        for i in 0 .. exp_types.length - 1 do
            for j in i + 1 .. exp_types.length - 1 do
                if exp_types[i].getType() != exp_types[j].getType()
                    msg = "Types are not consistent across collection"
                    mistatched_types(exp_types[i], msg)
                end
            end
        end
    end

    def analyze_confirmed_map(ast_node)
        elements = ast_node.getElements()
        key_types = Array.new()
        value_types = Array.new()
        for elem in elements do
            key = elem.getLhsExp()
            @main_analyzer.analyze_node_locally(key)
            key_type = @main_analyzer.getExpressionTypeToken()
            key_types.append(key_type)

            value = elem.getRhsExp()
            @main_analyzer.analyze_node_locally(value)
            value_type = @main_analyzer.getExpressionTypeToken()
            value_types.append(value_type)
        end
        if key_types.length != value_types.length
            raise Exception.new("Internal error, keys and values of map literal are different lengths")
        end
        for i in 0 .. key_types.length - 1 do
            for j in i .. key_types.length - 1 do
                if key_types[i].getType() != key_types[j].getType()
                    msg = "Key types are not consistent across collection"
                    make_and_send_error(key_types[i], msg)
                end
                if value_types[i].getType() != value_types[j].getType()
                    msg = "Value types are not consistent across collection"
                    make_and_send_error(value_types[i], msg)
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
# { 8 : 6, 7 : 57 }
# { 1, 2, 9, 6, 5 }
# [ 0, 1, 2, 3, 4, 5 ]