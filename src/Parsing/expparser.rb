require './tokentype.rb'
require_relative '../Tokenization/scanner.rb'
require_relative './parserutilities.rb'

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









































class PreFixExpression
    def initialize(token, operator, right_exp)
        @operator = operator
        @rhs_exp = right_exp
        @token = token
    end

    def _printLiteral(repr_list)
        repr_list.append("(")
        @rhs_exp._printLiteral(repr_list)
        repr_list.append(")")
    end

    def _printTokType(type_list)
        type_list.append("(")
        @rhs_exp._printLiteral(type_list)
        type_list.append(")")
    end

    def toJSON()
        return {
            "type" => "prefix",
            "token" => {
                "literal" => @token.getText(),
                "type" => @token.getType(),
                "line_number" => @token.getLine()
            },
            "rhs_exp" => @rhs_exp.toJSON()
        }
    end
end




class NameExpression
    def initialize(token)
        @token = token
        @checked = false
    end

    def get_name
        return @token.getText()
    end

    def getType
        return @token.getType()
    end

    def _printLiteral(repr_list)
        repr_list.append(get_name())
    end

    def _printTokType(type_list)
        type_list.append(@token.getType())
    end

    def toJSON()
        return {
            "type" => "identifier_or_literal",
            "token" => {
                "literal" => @token.getText(),
                "type" => @token.getType(),
                "line_number" => @token.getLine()
            }
        }
    end
end




class OperatorExpresison
    def initialize(token, lhs_exp, token_type, rhs_exp)
        @lhs = lhs_exp
        @rhs = rhs_exp
        @type = token_type
        @token = token
        @checked = false
    end

    def _printLiteral(repr_list)
        repr_list.append('(')
        @lhs._printLiteral(repr_list)
        repr_list.append(' ' + @token.getText() + ' ')
        @rhs._printLiteral(repr_list)
        repr_list.append(')')
    end

    def _printTokType(type_list)
        type_list.append('(')
        @lhs._printTokType(type_list)
        type_list.append(' ' + @type.to_s + ' ')
        @rhs._printTokType(type_list)
        type_list.append(')')
    end

    def toJSON()
        return {
            "type" => "binary",
            "token" => {
                "literal" => @token.getText(),
                "type" => @token.getType(),
                "line_number" => @token.getLine()
            },
            "lhs_exp" => @lhs.toJSON(),
            "rhs_exp" => @rhs.toJSON()
        }
    end
end





class CollectionExpression
    def initialize(left_bracket, elements, right_bracket)
        @left_bracket = left_bracket
        @elements = elements
        @right_bracket = right_bracket
        @checked = false
    end

    def _printLiteral(repr_list)
        repr_list.append(@left_bracket)
        i = 0
        l = @elements.length
        for elem in @elements do
            elem._printLiteral(repr_list)
            if(i < l - 1)
                repr_list.append(',')
            end
            i += 1
        end
        repr_list.append(@right_bracket)
    end

    def _printTokType(type_list)
        type_list.append(@left_bracket)
        i = 0
        l = @elements.length
        for elem in @elements do
            elem._printTokType(type_list)
            if(i < l - 1)
                type_list.append(',')
            end
            i += 1
        end
        type_list.append(@right_bracket)
    end

    def toJSON()
        elems = Array.new()
        for exp in @elements
            elems.append(exp.toJSON())
        end
        return {
            "type" => "collection",
            "left_delimiter" => @left_bracket,
            "right_delimiter" => @right_bracket,
            "elements" => elems
        }
    end
end




class MethodCallExpression
    def initialize(struct_name_token, methods)
        @struct_name = struct_name_token
        @methods = methods
    end

    def toJSON()
        jsonArgs = Array.new()
        for arg in @args
            jsonArgs.append(arg.toJSON())
        end
        return {
            "type" => "method_call",
            "struct" => @struct_name.toJSON(),
            "methods" => jsonArgs
        }
    end

    def _printLiteral(repr_list)
        @struct_name._printLiteral(repr_list)
        repr_list.append('(')
        i = 0
        l = @methods.length
        for meth in @methods do
            meth._printLiteral(repr_list)
            if(i < l - 1)
                repr_list.append(',')
            end
            i += 1
        end
        repr_list.append(')')
    end

    def _printTokType(type_list)
        @struct_name._printTokType(type_list)
        type_list.append('(')
        i = 0
        l = @methods.length
        for meth in @methods do
            meth._printTokType(type_list)
            if(i < l - 1)
                type_list.append(',')
            end
            i += 1
        end
        type_list.append(')')
    end
end

class CallExpression
    def initialize(token, expression, arguments)
        @function = expression
        @args = arguments
        @token = token
        @checked = false
    end

    def toJSON()
        jsonArgs = Array.new()
        for arg in @args
            jsonArgs.append(arg.toJSON())
        end
        return {
            "type" => "function_call",
            "name" => {
                "literal" => @token.getText(),
                "type" => @token.getType(),
                "line_number" => @token.getLine()
            },
            "lhs_exp" => @function.toJSON(),
            "arguments" => jsonArgs
        }
    end

    def _printLiteral(repr_list)
        @function._printLiteral(repr_list)
        repr_list.append('(')
        i = 0
        l = @args.length
        for arg in @args do
            arg._printLiteral(repr_list)
            if(i < l - 1)
                repr_list.append(',')
            end
            i += 1
        end
        repr_list.append(')')
    end

    def _printTokType(type_list)
        @function._printTokType(type_list)
        type_list.append('(')
        i = 0
        l = @args.length
        for arg in @args do
            arg._printTokType(type_list)
            if(i < l - 1)
                type_list.append(',')
            end
            i += 1
        end
        type_list.append(')')
    end
end