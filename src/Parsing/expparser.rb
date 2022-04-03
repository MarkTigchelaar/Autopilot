require './tokentype.rb'
require_relative '../keywords.rb'
require_relative '../Tokenization/scanner.rb'

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
        @prefixes = Hash.new()
        @prefix_parslets = Hash.new()
        @infixes = Hash.new()
        @infix_parslets = Hash.new()
        @root = nil
        @errorList = Array.new()
        @keyWords = getkeywords()
        register()
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
        elsif(tokIskeyword(token))
            #puts "token is a keyword, returning with nil"
            return nil
        end
        #puts "token literal: #{token.getText()}  #{token.getType()}"
        prefix = get_prefix_exp_parslet(token)
        #puts "prefix class: #{prefix.class}"
        if(hasErrors())
            return nil
        elsif(prefix == nil)
            #raise Exception.new("Could not parse prefix " + token.getText())
            addError(token, "Invalid constant or variable.")
            return nil
        end
        token = _next()
        #puts "token2 literal: #{token.getText()}  #{token.getType()}"
        left_exp = prefix.parse(self, token)
        #puts "                     :::: #{left_exp.class}"

        while(precedence < _get_precedence())
            token = _next()
            #puts "got next token: #{token.getText()}, #{token.getType()}"
            if(token == nil)
                break
            end
            infix = get_infix_exp_parslet(token)
            if(hasErrors())
                return nil
            elsif(infix == nil)
               raise Exception.new("Could not parse infix " + token.getText())
            end
            left_exp = infix.parse(self, left_exp, token)
            if(hasErrors())
                return nil
            end
        end
        return left_exp
    end

    def is_prefix(token)
        return @prefixes.has_key?(token.getText())
    end

    def get_prefix_exp_parslet(token)
        #puts "Token in get_prefix_exp_parslet: #{token.getText()} <#{token.getType()}>"
        keypresent = @prefixes.has_key?(token.getText())
        #puts "Key present? #{keypresent} "
        if(keypresent)
            key = @prefixes[token.getText()]
            if(@prefix_parslets.has_key?(key))
                return @prefix_parslets[key]
            else
                raise Exception.new("key " + key + " not found in prefix parslets")
            end
        elsif(isInt(token.getText()))
            return @prefix_parslets[INT]
        elsif(isFloat(token.getText()))
            return @prefix_parslets[FLOAT]
        elsif(@infixes.has_key?(token.getText()))
            #addError(token, "Operator not preceded by identifier")
            return nil
        else
            #puts "Token: #{token.getText()} #{token.getType()} is a ID"
            return @prefix_parslets[IDENTIFIER] 
        end
        return nil
    end

    # Does not determine if it is a "proper" identifier
    # checking if it is formed correctly (start with char of certain type) etc. is semantics


    def isInt(tokliteral)
        for i in 0 .. tokliteral.length-1 do
            if(!isDigit(tokliteral[i]))
                return false
            end
        end
        return true
    end

    def isFloat(tokliteral)
        decimal = 0
        for i in 0 .. tokliteral.length-1 do
            if(!isDigit(tokliteral[i]) and tokliteral[i] != '.')
                return false
            end
            if(tokliteral[i] == '.')
                decimal += 1
            end
        end
        if(decimal > 1)
            return false
        end
        return true
    end

    def isDigit(char)
        return ((char >= "0") and (char <= "9"))
    end

    def isAlpha(char)
        islowercase = (char.ord >= 'a'.ord && char.ord <= 'z'.ord)
        isuppercase = (char.ord >= 'A'.ord && char.ord <= 'Z'.ord)
        return (islowercase or isuppercase or char == '_')
    end

    def isAlphaNumeric(char)
        return (isAlpha(char) or isDigit(char))
    end

    def get_infix_exp_parslet(token)
        if(@infixes.has_key?(token.getText()))
            #puts "Token #{token.getText()} found in get_infix_exp_parslet"
            key = @infixes[token.getText()]
            if(@infix_parslets.has_key?(key))
                #puts " key found in infix parslets for #{token.getText()}, key: #{key}"
                return @infix_parslets[key]
            else
                raise Exception.new("key " + key + " not found in infix parslets")
            end
        end
        return nil
    end

    def _get_precedence
        if(_peek() == nil)
            return 0
        end
        #puts "calling get_infix_exp_parslet on peek, while inside _get_precedence for <#{_peek().getText()}>"
        infix = get_infix_exp_parslet(_peek())
        if(infix != nil)
            return infix.get_precedence()
        end
        #puts "infix is nil"
        return 0
    end

    def get_token_type(token)
        if(@prefixes.has_key?(token.getText()))
            return @prefixes[token.getText()]
        elsif(@infixes.has_key?(token.getText()))
            return @infixes[token.getText()]
        else
            raise Exception.new("Parser cannot find token type of " + token.getText())
        end
    end

    def tokIskeyword(token)
        return (@keyWords.has_key?(token.getText()) or @keyWords.has_key?(token.getType()))
    end

    def discard(expected_literal)
        token = _peek()
        if(token.getText() != expected_literal)
            raise Exception.new("Expected token " + expected_literal + ", got " + token.getText())
        end
        token = _next()
    end

    def register()

        @prefixes['-'] = MINUS
        @prefix_parslets[MINUS] = PrefixOperatorParselet.new(PREFIX)

        nameParser = NameParslet.new()
        @prefix_parslets[INT] = nameParser 
        @prefix_parslets[FLOAT] = nameParser
        @prefix_parslets[IDENTIFIER] = nameParser

        @prefixes['('] = LEFT_PAREN
        @prefix_parslets[LEFT_PAREN] = GroupParselet.new('(', ')')

        @prefixes['['] = LEFT_BRACKET
        @prefix_parslets[LEFT_BRACKET] = CollectionParslet.new('[', ']') # collectionParslet
        
        @prefixes['{'] = LEFT_BRACE
        @prefix_parslets[LEFT_BRACE] = CollectionParslet.new('{', '}')

        @infixes['+'] = PLUS
        @infix_parslets[PLUS] = BinaryOperatorParselet.new(SUM, false)

        @infixes['-'] = MINUS
        @infix_parslets[MINUS] = BinaryOperatorParselet.new(SUM, false)

        @infixes['*'] = STAR
        @infix_parslets[STAR] = BinaryOperatorParselet.new(PRODUCT, false)

        @infixes['/'] = SLASH
        @infix_parslets[SLASH] = BinaryOperatorParselet.new(PRODUCT, false)

        @infixes['%'] = MOD
        @infix_parslets[MOD] = BinaryOperatorParselet.new(PRODUCT, false)

        @infixes['^'] = CARROT
        @infix_parslets[CARROT] = BinaryOperatorParselet.new(EXPONENT, true)
        
        @infixes[':'] = COLON
        @infix_parslets[COLON] = BinaryOperatorParselet.new(HASHLITERAL, false)

        @infixes['<'] = LESS
        @infix_parslets[LESS] = BinaryOperatorParselet.new(CONDITIONAL, false)

        @infixes['<='] = LESS_EQUAL
        @infix_parslets[LESS_EQUAL] = BinaryOperatorParselet.new(CONDITIONAL, false)

        @infixes['>'] = GREATER
        @infix_parslets[GREATER] = BinaryOperatorParselet.new(CONDITIONAL, false)

        @infixes['>='] = GREATER_EQUAL
        @infix_parslets[GREATER_EQUAL] = BinaryOperatorParselet.new(CONDITIONAL, false)

        @infixes['=='] = EQUAL_EQUAL
        @infix_parslets[EQUAL_EQUAL] = BinaryOperatorParselet.new(CONDITIONAL, false)

        @infixes['!='] = BANG_EQUAL
        @infix_parslets[BANG_EQUAL] = BinaryOperatorParselet.new(CONDITIONAL, false)

        @infixes['and'] = AND
        @infix_parslets[AND] = BinaryOperatorParselet.new(LOGICAL, false)

        @infixes['nand'] = NAND
        @infix_parslets[NAND] = BinaryOperatorParselet.new(LOGICAL, false)

        @infixes['or'] = OR
        @infix_parslets[OR] = BinaryOperatorParselet.new(LOGICAL, false)

        @infixes['nor'] = NOR
        @infix_parslets[NOR] = BinaryOperatorParselet.new(LOGICAL, false)

        @infixes['xor'] = XOR
        @infix_parslets[XOR] = BinaryOperatorParselet.new(LOGICAL, false)

        @infixes['not'] = NOT
        @infix_parslets[NOT] = BinaryOperatorParselet.new(LOGICAL, false)

        @infixes['('] = "CALL"
        @infix_parslets["CALL"] = CallParselet.new()
    end


    def addError(token, message)
        err = Hash.new()
        err["file"] = token.getFilename()
        err["tokenLiteral"] = token.getText()
        err["lineNumber"] = token.getLine()
        err["message"] = message
        @errorList.append(err)
        @hasErrors = true
    end
end












class PrefixOperatorParselet
    def initialize(precedence)
        @precedence = precedence
    end

    def parse(parser, token)
        err = MISSING_EXP_CONST_VAR
        if(parser.hasErrors())
            return nil
        end
        #puts "parsing prefix with token: #{token.getText()}"
        peek = parser._peek()
        #if(peek.getType() == "EOF")
        #    parser.addError(token, err)
        #    return
        #end
        #puts "calling parse from Prefix parser on next token: #{peek.getText()}"
        if(parser.is_prefix(peek))
            parser.addError(token, err)
            return nil
        end 
        rhs = parser._parse(@precedence)
        #puts "RIGHT HAND SIDE CLASS: #{rhs.class}"
        #puts "done parsing prefix"
        #if(rhs == nil)
        #    parser.addError(token, err)
        #end
        #rhs.checkForErrors(parser)
        #puts "#{rhs.class}  #{rhs.get_name()}"
        #if(parser.hasErrors())
        #    return nil
        #end
        prefix = PreFixExpression.new(token, parser.get_token_type(token), rhs)
        prefix.checkForErrors(parser)
        return prefix
    end

    def get_precedence
        return @precedence
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

    def checkForErrors(parser)
        if(@checked)
            return false
        elsif(@rhs_exp == nil ) # or @rhs_exp.getType() == "EOF"
            parser.addError(@token, MISSING_EXP_CONST_VAR)
            #puts "HERE ADDING A ERROR FOR RHS"
            return true
        elsif(@rhs_exp.checkForErrors(parser))
            return true
        end
        @checked = true
        return false
    end
end

class NameParslet

    def parse(parser, token)
        if(parser.hasErrors())
            return nil
        end
        #puts"------ parsing name expresison"
        nameExp = NameExpression.new(token)
        nameExp.checkForErrors(parser)
        return nameExp
    end
end


class NameExpression
    def initialize(token)
        #puts "initilizing name expression for #{token.getText()} #{token.getType()}"
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

    def checkForErrors(parser)
        err = "Invalid variable name, keywords cannot be used as variable names."
        if(@checked)
            return false
        end
        @checked = true
        if(@token.getType() == "EOF")
            parser.addError(@token, "End of file reached while parsing expression")
            return true
        elsif(parser.tokIskeyword(@token))
            parser.addError(@token, err)
            return true
        end
        
        return false
    end
end

class GroupParselet
    def initialize(open_char, close_char)
        @open_char = open_char
        @close_char = close_char
    end

    def parse(parser, token)
        if(parser.hasErrors())
            return nil
        end
        if(token.getText() != @open_char)
            raise Exception.new("Expected " + @open_char + " for group expression, found " + token.getText())
        end
        #puts "parsing group expression, parsing inner exp"
        expression = parser.parse_expression()
        if(parser.hasErrors())
            return nil
        end
        parser.discard(@close_char)
        #puts "done parsing group expression, parsed inner exp"
        expression.checkForErrors(parser)
        return expression
    end
end

class BinaryOperatorParselet
    def initialize(precedence=0, right_assoc=false)
        @precedence = precedence
        @right_assoc = right_assoc
    end

    def parse(parser, lhs_exp, token)
        if(parser.hasErrors())
            return nil
        end
        modifier = 0
        if(@right_assoc)
            modifier += 1
        end
        #puts "parsing BinaryOperator #{token.getText()}"
        plevel = @precedence - modifier
        rhs_exp = parser._parse(plevel)
        if(parser.hasErrors())
            return nil
        end
        #puts "parsed the right hand expression"
        token_type = parser.get_token_type(token)
        #puts "token type: #{token_type} #{token.getText()}"
        opExp = OperatorExpresison.new(token, lhs_exp, token_type, rhs_exp)
        opExp.checkForErrors(parser)
        return opExp
    end

    def get_precedence
        return @precedence
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

    def checkForErrors(parser)
        if(@checked)
            return
        elsif(@lhs == nil)
            parser.addError(@token, MISSING_EXP_CONST_VAR)
            return true
        elsif(@rhs == nil)
            parser.addError(@token, MISSING_EXP_CONST_VAR)
            return true
        elsif(@lhs.checkForErrors(parser))
            return true
        elsif(@rhs.checkForErrors(parser))
            return true
        end
        @checked = true
        #puts "HERE AT END"
        return false
    end
end

class CollectionParslet

    def initialize(left_bracket, right_bracket)
        @left_bracket = left_bracket
        @right_bracket = right_bracket
    end

    def parse(parser, token)
        if(parser.hasErrors())
            return nil
        end
        #puts "parsing collection, first token = #{token.getText()} #{token.getType()}" 
        elements = Array.new()
        if(parser._peek().getText() != @right_bracket)
            
            while(true)
                #puts "          next token #{parser._peek().getText()}"
                elements.append(parser.parse_expression())
                if(parser.hasErrors())
                    return nil
                end
                if(parser._peek().getText() != ',')
                    break
                else
                    parser.discard(',')
                end
            end
            if(parser._peek().getText() != @right_bracket)
                raise Exception.new("FATAL! in file #{parser._peek().getFilename()} Unkown token " + parser._peek().getText() + ". Expected #{@right_bracket}")
            end
            
        end
        #puts "discarding #{@right_bracket}"
        parser.discard(@right_bracket)
        colExp =  CollectionExpresison.new(@left_bracket, elements, @right_bracket)
        colExp.checkForErrors(parser)
        return colExp
    end

    def get_precedence
        return CALL
    end
end

class CollectionExpresison
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

    def checkForErrors(parser)
        if(@checked)
            return true
        end
        return false
    end
end

class CallParselet

    def parse(parser, lhs_exp, token)
        if(parser.hasErrors())
            return nil
        end
        arguments = Array.new()
        #puts "parsing call expression"
        if(parser._peek().getText() != ')')
            #puts "not a empty function call: #{parser._peek().getText()}"
            while(true)
                #puts "parsing arg ..."
                arguments.append(parser.parse_expression())
                if(parser.hasErrors())
                    return nil
                end
                if(parser._peek().getText() != ',')
                    break
                else
                    #puts "found , discarding"
                    parser.discard(',')
                end
            end
            if(parser._peek().getText() != ')')
                raise Exception.new("Unkown token " + parser._peek().getText() + ". Expected )")
            end
        else
            #puts "no args in function call" 
        end
        #puts "discarding )"
        parser.discard(')')
        callExp = CallExpression.new(token, lhs_exp, arguments)
        callExp.checkForErrors(parser)
        return callExp
    end

    def get_precedence
        return CALL
    end
end

class CallExpression
    def initialize(token, expression, arguments)
        #puts "initializing call expression with #{expression.get_name()}"
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

    def checkForErrors(parser)
        if(@checked)
            return true
        end
        return false
    end
end