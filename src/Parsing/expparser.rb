require './tokentype.rb'
#require_relative '../keywords.rb'
require_relative '../Tokenization/scanner.rb'
require_relative './parserutilities.rb'

HASHLITERAL = 1
LOGICAL     = 2
CONDITIONAL = 3
SUM         = 4
PRODUCT     = 5
EXPONENT    = 6
PREFIX      = 7
POSTFIX     = 8
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
        ast = _parse(0)
        if hasErrors()
            return nil
        end
        return ast
    end

    def done
        @tokenizer.closeSource()
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
        #expr_list.append("(")
        expr_list = @root._printLiteral(expr_list)
        #expr_list.append(")")
        concact_all_strings = ""
        return expr_list.join(concact_all_strings)
    end

    def tokenTypeString
        type_list = Array.new()
        #type_list.append("(")
        type_list = @root._printTokType(type_list)
        #type_list.append(")")
        concact_all_strings = ""
        return type_list.join(concact_all_strings)
    end

    def getErrorList
        return @errorList
    end

    def hasErrors
        return @errorList.length > 0
    end

    def _next
        tok = @tokenizer.nextToken()
        return tok
    end

    def _peek
        return @tokenizer.peekToken()
    end

    def _parse(precedence)
        token = _peek()
        if(token == nil)
            return nil
        end
        left_exp = parse_prefix_expression()
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
        rhs = _parse(PREFIX)
        return PreFixExpression.new(token, MINUS, rhs)
    end

    def parse_parenthesis()
        exp = parse_expression()
        discard(')')
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
        if(_peek().getText() != end_char)
            while(true)
                exp = parse_expression()
                array_elements.append(exp)
                if(_peek().getType() != COMMA)
                    break
                else
                    discard(',')
                end
            end
        end
        discard(end_char)
        return CollectionExpression.new(start_char, array_elements, end_char)
    end

    def parse_name(token)
        # check if it's any type of keyword, including ) ] } .. etc.
        if(isExternalKeyword(token) || is_interal_statement_keyword(token))
            msg = "Unexpected token #{token.getText()}."
            addError(token, msg)
        end
        return NameExpression.new(token)
    end

    def parse_infix_sub_tree(precedence, left_exp)
        while(precedence < _get_infix_precedence())
            token = _next()
            if(token == nil)
                break
            end
            left_exp = parse_infix_expression(token, left_exp)
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
        else
            msg = "Can't find infix"
            addError(token, msg)
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

    def parse_function_call(left_exp, token)
        func_args = Array.new()
        if(_peek().getType() != RIGHT_PAREN)
            while(true)
                exp = parse_expression()
                func_args.append(exp)
                if(_peek().getType() != COMMA)
                    break
                else
                    discard(',')
                end
            end
        end
        discard(')')
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
        when LEFT_PAREN
            CALL
        else
            0
        end
    end

    def tokIskeyword(token)
        return isGeneralKeyWord(token.getText())
    end

    def discard(expected_literal)
        token = _peek()
        if(token.getText() != expected_literal)
            raise Exception.new("Expected token " + expected_literal + ", got " + token.getText())
        end
        token = _next()
    end

    def addError(token, message)
        @tokenizer.addError(token, message)
        err = Hash.new()
        err["file"] = token.getFilename()
        err["tokenLiteral"] = token.getText()
        err["lineNumber"] = token.getLine()
        err["message"] = message
        @errorList.append(err)
        @hasErrors = true
    end
end






class PreFixExpression
    def initialize(token, operator, right_exp)
        @operator = operator
        @rhs_exp = right_exp
        @token = token
        @checked = false
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
end






class CallExpression
    def initialize(token, expression, arguments)
        @function = expression
        @args = arguments
        @token = token
        @checked = false
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
        #for i in 0 .. l do
            arg._printTokType(type_list)
            if(i < l - 1)
                type_list.append(',')
            end
            i += 1
        end
        type_list.append(')')
    end
end