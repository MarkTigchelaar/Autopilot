require './tokentype.rb'
require_relative './parserutilities.rb'
require_relative '../ASTComponents/ExpressionComponents/call_expression.rb'
require_relative '../ASTComponents/ExpressionComponents/method_call_expression.rb'
require_relative '../ASTComponents/ExpressionComponents/collection_expression.rb'
require_relative '../ASTComponents/ExpressionComponents/operator_expression.rb'
require_relative '../ASTComponents/ExpressionComponents/name_expression.rb'
require_relative '../ASTComponents/ExpressionComponents/prefix_expression.rb'

HASHLITERAL = 1
LOGICAL     = 2
CONDITIONAL = 3
SUM         = 4
PRODUCT     = 5
EXPONENT    = 6
STRUCTFIELD = 7
PREFIX      = 8
POSTFIX     = 9
CALL        = 10

MISSING_EXP_CONST_VAR = "Operator is missing constant, variable or expression."

# Pratt Parser
class ExpressionParser
    def initialize
        @name = nil
        @tokenizer = nil
        @root = nil
        @errorList = Array.new()
    end

    def reset()
        @name = nil
        @tokenizer = nil
        @root = nil
    end
    
    def loadTokenizer(toks)
        reset()
        @tokenizer = toks
    end

    def parseFile
        @root = parse_expression()
        done()
    end

    def parse_expression
        @errorList = Array.new()
        ast = _parse(0)
        if hasErrors()
            return nil
        end
        return ast
    end

    def done
        @tokenizer.closeSource()
    end

    def _next
        tok = @tokenizer.nextToken()
        return tok
    end

    def nextToken()
        _next()
    end

    def discard()
        _next()
    end

    def _peek
        return @tokenizer.peekToken()
    end

    def peek()
        _peek()
    end

    def setToSync()
        internalSynchronize(self)
    end

    def _parse(precedence)
        token = _peek()
        if(token == nil)
            raise Exception.new("INCORRECT!")
        end
        if(hasErrors())
            return nil
        end
        left_exp = parse_prefix_expression()
        if(left_exp == nil)
            return nil
        end
        if(hasErrors())
            return nil
        end
        return parse_infix_sub_tree(precedence, left_exp)
    end

    def parse_prefix_expression()
        token = _next()
        return case token.getType()
        when MINUS
            parse_minus_prefix(token)
        when LEFT_PAREN
            parse_parenthesis()
        when LEFT_BRACKET
            parse_brackets()
        when LEFT_BRACE
            parse_curly_braces()
        else
            parse_name(token)
        end
    end

    def parse_minus_prefix(token)
        if(isEOF(_peek()))
            eofReached(self)
            return nil
        elsif(!isIdentifier(_peek()))
            msg = "Unexpected token #{token.getText()}."
            addError(token, msg)
            return nil
        end
        rhs = _parse(PREFIX)
        return PreFixExpression.new(token, MINUS, rhs)
    end

    def parse_parenthesis()
        if(_peek().getType == RIGHT_PAREN)
            msg = "Empty Expression."
            self.addError(_peek(), msg)
            return nil
        elsif(isEOF(_peek()))
            eofReached(self)
            return nil
        end

        exp = parse_expression()

        if(isEOF(_peek()))
            eofReached(self)
            return nil
        elsif(_peek().getType != RIGHT_PAREN)
            unexpectedToken(self)
            return nil
        end
        discardToken(')')
        return exp
    end

    def parse_brackets()
        return parse_collection('[', ']')
    end

    def parse_curly_braces()
        return parse_collection('{', '}')
    end

    def parse_collection(start_char, end_char)
        array_elements = Array.new
        if(isEOF(_peek()))
            eofReached(self)
            return nil
        end
        if(_peek().getText() != end_char)
            while(true)
                if([COMMA, RIGHT_PAREN, RIGHT_BRACKET, RIGHT_BRACE].include?(_peek().getType()))
                    unexpectedToken(self)
                    return nil
                end
                exp = parse_expression()
                array_elements.append(exp)
                if(_peek().getType() != COMMA)
                    break
                else
                    discardToken(',')
                end
            end
        end
        if(isEOF(_peek()))
            eofReached(self)
            return nil
        elsif(_peek().getText() != end_char)
            unexpectedToken(self)
            return nil
        end
        discardToken(end_char)
        return CollectionExpression.new(start_char, array_elements, end_char)
    end

    def parse_name(token)
        # check if it's any type of keyword, including ) ] } .. etc.
        if(isExternalKeyword(token) || is_interal_statement_keyword(token))
            msg = "Unexpected token #{token.getText()}."
            self.addError(token, msg)
        elsif(isScopeKeyword(token))
            msg = "Unexpected token #{token.getText()}."
            self.addError(token, msg)
        elsif(isOperator(token))
            msg = "Invalid constant or variable."
            self.addError(token, msg)
        elsif(isPrimitiveType(token, true))
            msg = "Unexpected token #{token.getText()}."
            self.addError(token, msg)
        elsif(isEOF(token))
            eofReached(self)
        end
        return NameExpression.new(token)
    end

    def parse_infix_sub_tree(precedence, left_exp)
        if(hasErrors())
            return nil
        end
        while(precedence < _get_infix_precedence())
            token = _next()
            if(token == nil)
                break
            end
            left_exp = parse_infix_expression(token, left_exp)
            if(hasErrors())
                return nil
            end
            if(left_exp == nil)
               raise Exception.new("Could not parse infix " + token.getText())
            end
        end
        return left_exp
    end

    def parse_infix_expression(token, left_exp)
        return case token.getType()
        when PLUS, MINUS
            parse_binary_operator(SUM, left_exp, token)
        when STAR, SLASH, MOD
            parse_binary_operator(PRODUCT, left_exp, token)
        when CARROT
            parse_binary_operator(EXPONENT, left_exp, token, true)
        when COLON
            parse_binary_operator(HASHLITERAL, left_exp, token)
        when LESS, LESS_EQUAL, GREATER, GREATER_EQUAL, EQUAL_EQUAL, BANG_EQUAL
            parse_binary_operator(CONDITIONAL, left_exp, token)
        when AND, NAND, OR, NOR, XOR, NOT
            parse_binary_operator(LOGICAL, left_exp, token)
        when LEFT_PAREN
            parse_function_call(left_exp, token)
        when DOT
            parse_method_call(left_exp, token)
        else
            msg = "Can't find infix"
            self.addError(token, msg)
            nil
        end
    end

    def parse_binary_operator(precedence, lhs_exp, token, right_associative = false)
        if(right_associative)
            precedence -= 1
        end
        rhs_exp = _parse(precedence)
        return OperatorExpresison.new(token, lhs_exp, token.getType(), rhs_exp)
    end

    def parse_method_call(left_exp, token)
        method_list = Array.new()
        while(token.getType() == DOT)
            method = _parse(0)
            method_list.append(method)
            token = _next()
        end
        return MethodCallExpression.new(left_exp, method_list)
    end

    def parse_function_call(left_exp, token)
        func_args = Array.new()
        if(_peek().getType() != RIGHT_PAREN)
            while(true)
                if(_peek().getType() == COMMA)
                    unexpectedToken(self)
                    return nil
                end
                exp = parse_expression()
                if(hasErrors())
                    return nil
                end
                func_args.append(exp)
                if(_peek().getType() != COMMA)
                    break
                else
                    discardToken(',')
                end
            end
        end
        if(isEOF(_peek()))
            eofReached(self)
            return nil
        end
        discardToken(')')
        return CallExpression.new(token, left_exp, func_args)
    end

    def _get_infix_precedence
        if(_peek() == nil)
            return 0
        end
        return case _peek().getType()
        when PLUS, MINUS
            SUM
        when STAR, SLASH, MOD
            PRODUCT
        when CARROT
            EXPONENT
        when COLON
            HASHLITERAL
        when LESS, LESS_EQUAL, GREATER, GREATER_EQUAL, EQUAL_EQUAL, BANG_EQUAL
            CONDITIONAL
        when AND, NAND, OR, NOR, XOR, NOT
            LOGICAL
        when DOT
            STRUCTFIELD
        when LEFT_PAREN
            CALL
        else
            0
        end
    end

    def tokIskeyword(token)
        return isGeneralKeyWord(token.getText())
    end

    def discardToken(expected_literal)
        token = _peek()
        if(token.getText() != expected_literal)
            raise Exception.new("Expected token " + expected_literal + ", got " + token.getText())
        end
        token = _next()
    end

    public def addError(token, message)
        # Sign of refactoring needed, or sign that
        # code is designed to be tested?
        # Both? I must have Covid, 
        # since I can't tell if this is a code smell.
        regular_parser = @tokenizer.class.name == "Parser"
        test_parser = @tokenizer.class.name == "DummyParser"
        if(regular_parser || test_parser)
            @tokenizer.addError(token, message)
        end
        err = Hash.new()
        err["file"] = token.getFilename()
        err["tokenLiteral"] = token.getText()
        err["lineNumber"] = token.getLine()
        err["message"] = message
        @errorList.append(err)
    end

    def loadFile(filename)
        @name = filename
        @tokenizer.loadSource(filename)
    end

    def getFilename
        return @name
    end

    def astString
        expr_list = Array.new()
        expr_list = @root._printLiteral(expr_list)
        concact_all_strings = ""
        return expr_list.join(concact_all_strings)
    end

    def tokenTypeString
        type_list = Array.new()
        type_list = @root._printTokType(type_list)
        concact_all_strings = ""
        return type_list.join(concact_all_strings)
    end

    def getErrorList
        dup_indicies = Set.new
        for i in (@errorList.length - 1).downto(0) do
            for j in (i - 1).downto(0) do
                if(i == j)
                    next
                end
                b = @errorList[j]
                same_file = @errorList[i]["file"] == b["file"]
                same_lit = @errorList[i]["tokenLiteral"] == b["tokenLiteral"]
                same_line = @errorList[i]["lineNumber"] == b["lineNumber"]
                same_msg = @errorList[i]["message"] == b["message"]
                is_eof = b["message"] == "End of file reached."
                if(same_file and same_lit and same_line and same_msg and is_eof)
                    dup_indicies.add(i)
                end
            end
        end
        for i in (@errorList.length - 1).downto(0) do
            if dup_indicies.include?(i)
                @errorList.delete_at(i)
            end
        end

        return @errorList
    end

    def hasErrors
        return @errorList.length > 0
    end
end
