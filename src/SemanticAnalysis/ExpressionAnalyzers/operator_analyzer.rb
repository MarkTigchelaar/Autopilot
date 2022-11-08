class OperatorExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
        @returns_bools = ["<", "<=", ">", ">=", "==", "!=", "and", "nand", "or", "nor", "xor", "not"]
    end

    def analyze_node_locally(ast_node)
        lhs_good = false
        rhs_good = false
        operator = ast_node.getOperator()

        @main_analyzer.analyze_node_locally(ast_node.getLhsExp())
        lhsType = @main_analyzer.getExpressionTypeToken()
        saved_lhs_invalid_exp_type = nil
        if @main_analyzer.astSubTreeCompatableWithOperator(operator)
            lhs_good = true
        else
            msg = "Operator \"#{operator.getText()}\" cannot be applied to left hand side expression of type \"#{lhsType.getType().downcase()}\""
            make_and_send_error(ast_node.getName(), msg)
            set_expression_to_invalid(lhsType)
            saved_lhs_invalid_exp_type = @main_analyzer.getExpressionTypeToken()
        end

        
        @main_analyzer.analyze_node_locally(ast_node.getRhsExp())
        rhsType = @main_analyzer.getExpressionTypeToken()
        if @main_analyzer.astSubTreeCompatableWithOperator(operator)
            rhs_good = true
        else
            msg = "Operator \"#{operator.getText()}\" cannot be applied to right hand side expression of type \"#{rhsType.getType().downcase()}\""
            make_and_send_error(ast_node.getName(), msg)
            # bc issue starts at left side token:
            #@main_analyzer.setExpressionTypeToken(lhsType)
            set_expression_to_invalid(rhsType)
        end
        if !saved_lhs_invalid_exp_type.nil?
            @main_analyzer.setExpressionTypeToken(saved_lhs_invalid_exp_type)
        end

        if lhs_good and rhs_good
            if are_compatable_types(lhsType, rhsType)
                set_compatable_mismatched_types(lhsType, rhsType, operator)
            else
                msg = "Type \"#{lhsType.getType().downcase()}\" not compatable with type \"#{rhsType.getType().downcase()}\""
                make_and_send_error(ast_node.getName(), msg)
                set_expression_to_invalid(lhsType)
            end
        end
    end

    def set_compatable_mismatched_types(lhsType, rhsType, operator)
        if makes_string(lhsType, rhsType, operator)
            make_and_set_string(lhsType, rhsType, operator)
        elsif makes_int(lhsType, rhsType, operator)
            make_and_set_int(lhsType, rhsType, operator)
        elsif makes_long(lhsType, rhsType, operator)
            make_and_set_long(lhsType, rhsType, operator)
        elsif makes_float(lhsType, rhsType, operator)
            make_and_set_float(lhsType, rhsType, operator)
        elsif makes_double(lhsType, rhsType, operator)
            make_and_set_double(lhsType, rhsType, operator)
        elsif makes_bool(lhsType, rhsType, operator)
            make_and_set_bool(lhsType, rhsType, operator)
        else
            raise Exception.new("INTERNAL ERROR: unresolved types: #{lhsType.getType()} #{rhsType.getType()}")
        end
    end

    def makes_string(lhsType, rhsType, operator)
        return false if makes_bool(lhsType, rhsType, operator)
        if [STRING, CHAR].include?(lhsType.getType()) && [STRING, CHAR].include?(rhsType.getType())
            return true
        end
        return false
    end

    def make_and_set_string(lhsType, rhsType, operator)
        literal = operator.getText() #lhsType.getText() + " " + operator.getText() + " " + rhsType.getText()
        newString = Token.new(STRING, literal, literal, lhsType.getLine(), lhsType.getFilename())
        @main_analyzer.setExpressionTypeToken(newString)
    end

    def makes_int(lhsType, rhsType, operator)
        return false if makes_bool(lhsType, rhsType, operator)
        if [INT].include?(lhsType.getType()) && [INT].include?(rhsType.getType())
            return true
        end
        return false
    end

    def make_and_set_int(lhsType, rhsType, operator)
        literal = operator.getText() # lhsType.getText() + " " + operator.getText() + " " + rhsType.getText()
        newString = Token.new(INT, literal, literal, lhsType.getLine(), lhsType.getFilename())
        @main_analyzer.setExpressionTypeToken(newString)
    end

    def makes_long(lhsType, rhsType, operator)
        return false if makes_bool(lhsType, rhsType, operator)
        if [INT, LONG].include?(lhsType.getType()) && [INT, LONG].include?(rhsType.getType())
            return true
        end
        return false
    end

    def make_and_set_long(lhsType, rhsType, operator)
        literal = operator.getText() # lhsType.getText() + " " + operator.getText() + " " + rhsType.getText()
        newString = Token.new(LONG, literal, literal, lhsType.getLine(), lhsType.getFilename())
        @main_analyzer.setExpressionTypeToken(newString)
    end

    def makes_float(lhsType, rhsType, operator)
        return false if makes_bool(lhsType, rhsType, operator)
        if [FLOAT].include?(lhsType.getType()) && [FLOAT].include?(rhsType.getType())
            return true
        end
        return false
    end

    def make_and_set_float(lhsType, rhsType, operator)
        literal = operator.getText() #lhsType.getText() + " " + operator.getText() + " " + rhsType.getText()
        newDouble = Token.new(FLOAT, literal, literal, lhsType.getLine(), lhsType.getFilename())
        @main_analyzer.setExpressionTypeToken(newDouble)
    end

    def makes_double(lhsType, rhsType, operator)
        return false if makes_bool(lhsType, rhsType, operator)
        if [FLOAT, DOUBLE].include?(lhsType.getType()) && [FLOAT, DOUBLE].include?(rhsType.getType())
            return true
        end
        return false
    end

    def make_and_set_double(lhsType, rhsType, operator)
        literal = operator.getText() #lhsType.getText() + " " + operator.getText() + " " + rhsType.getText()
        newDouble = Token.new(DOUBLE, literal, literal, lhsType.getLine(), lhsType.getFilename())
        @main_analyzer.setExpressionTypeToken(newDouble)
    end

    def makes_bool(lhsType, rhsType, operator)
        if @returns_bools.include?(operator.getText())
            return true
        end
        return false
    end

    def make_and_set_bool(lhsType, rhsType, operator)
        literal = operator.getText() #lhsType.getText() + " " + operator.getText() + " " + rhsType.getText()
        newBool = Token.new(BOOL, literal, literal, lhsType.getLine(), lhsType.getFilename())
        @main_analyzer.setExpressionTypeToken(newBool)
    end

    def set_expression_to_invalid(rvalue_type)
        literal = rvalue_type.getText()
        invalid = Token.new(nil, literal, literal, rvalue_type.getLine(), rvalue_type.getFilename())
        @main_analyzer.setExpressionTypeToken(invalid)
    end

    def are_compatable_types(lhsType, rhsType)
        compatable_types = [
            ["int", "long"],
            ["int", "int"],
            ["long", "long"],
            ["long", "int"],
            ["char", "char"],
            ["char", "string"],
            ["string", "char"],
            ["string", "string"],
            ["float", "float"],
            ["float", "double"],
            ["double", "float"],
            ["double", "double"],
            ["bool", "bool"]
        ]
        for i in 0 .. compatable_types.length - 1
            if lhsType.getType().downcase() == compatable_types[i][0] && rhsType.getType().downcase() == compatable_types[i][1]
                return true
            end
        end
        return false
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
