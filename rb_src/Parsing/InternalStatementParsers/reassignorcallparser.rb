require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'
require_relative '../../ASTComponents/InternalStatementComponents/reassign_or_call_statement.rb'

class ReassignOrCallParser
    def initialize(expression_parser)
        @expression_parser = expression_parser
        @var_name = nil
        @index_token = nil
        @assignment_operator = nil
        @expression_ast = nil
        @functions = Array.new
    end

    def parse(parser)
        errCount = parser.errorCount()
        reset()
        name = parser.nextToken()
        enforceIdentifier(name)
        peekTok = parser.peek()
        assignment_type_token = nil
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(
            [
                EQUAL, PLUS_EQUAL, 
                MINUS_EQUAL, STAR_EQUAL, 
                SLASH_EQUAL, CARROT_EQUAL, MOD_EQUAL
            ].include?(peekTok.getType())
            )
            @var_name = name
            assignment_type_token = peekTok
            equalStep(parser)
        elsif(peekTok.getType() == LEFT_PAREN)
            callFuncStep(parser, name)
        elsif(peekTok.getType() == DOT)
            @var_name = name
            dotStep(parser)
        elsif(peekTok.getType() == LEFT_BRACKET)
            left_bracket_step(parser)
        else
            unexpectedToken(parser)
        end
        r = ReassignmentOrCallStatement.new(@var_name, assignment_type_token, @expression_ast, @functions, @index_token, @assignment_operator)
        reset()
        if(errCount < parser.errorCount())
            internalSynchronize(parser)
        end
        return r
    end

    def equalStep(parser)
        @assignment_operator = parser.nextToken()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or is_boolean_keyword(peekTok))
            parseExpression(parser)
        elsif(isInt(peekTok) or isFloat(peekTok))
            parseExpression(parser)
        elsif(is_string_or_char(peekTok))
            parseExpression(parser)
        else
            unexpectedToken(parser)
        end
    end

    def parseExpression(parser)
        @expression_parser.loadTokenizer(parser)
        @expression_ast = @expression_parser.parse_expression()
    end

    def callFuncStep(parser, name)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
            return
        elsif(peekTok.getType() != RIGHT_PAREN and !isValidIdentifier(peekTok) and peekTok.getType() != STRING and peekTok.getType() != CHAR)
            unexpectedToken(parser)
            return
        end
        args = Array.new
        @expression_parser.loadTokenizer(parser)
        while(!isEOF(peekTok) and peekTok.getType() != RIGHT_PAREN)
            ast = @expression_parser.parse_expression()
            args.append(ast)
            peekTok = parser.peek()
            if(isEOF(peekTok))
                eofReached(parser)
                return
            elsif(peekTok.getType() == COMMA)
                parser.discard()
                peekTok = parser.peek()
            elsif(peekTok.getType() == RIGHT_PAREN)
                break
            else
                unexpectedToken(parser)
                return
            end
        end
        @functions.append(FuncCall.new(name, args))
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == RIGHT_PAREN)
            callEndStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def callEndStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(peekTok.getType() == DOT)
            dotStep(parser)
        end
    end

    def dotStep(parser)
        parser.discard()
        peekTok = parser.peek()
        # name for "method call"
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            funcNameStep(parser, peekTok)
        else
            unexpectedToken(parser)
        end
    end

    def funcNameStep(parser, name)
        parser.discard()
        peekTok = parser.peek()
        # name for "method call"
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == LEFT_PAREN)
            callFuncStep(parser, name)
        #elsif( ... == LEFT_bracket)
            # index_access_step()
        #elsif(... == DOT)
        # is a public field
            # dotStep()
        else
            unexpectedToken(parser)
        end
    end

    def left_bracket_step(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) || peekTok.getType() == INT || peekTok.getType() == LONG)
            index_step(parser)
        else
            unexpectedToken(parser)
        end
    end

    def index_step(parser)
        @index_token = parser.nextToken()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == RIGHT_BRACKET)
            right_bracket_step(parser)
        else
            unexpectedToken(parser)
        end    
    end

    def right_bracket_step(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(
            [
                EQUAL, PLUS_EQUAL, 
                MINUS_EQUAL, STAR_EQUAL, 
                SLASH_EQUAL, CARROT_EQUAL, MOD_EQUAL
            ].include?(peekTok.getType())
            )
            equalStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def reset
        @var_name = nil
        @index_token = nil
        @assignment_operator = nil
        @expression_ast = nil
        @functions = Array.new
        @expression_parser.reset()
    end

    def enforceIdentifier(token)
        if(!isValidIdentifier(token))
            throw Exception.new("Did not enounter \"valid identifier\" in file " + token.getFilename() + ", got #{token.getText()}")
        end
    end
end

class FuncCall
    def initialize(name, args)
        @name = name
        @args = args
    end

    def toJSON()
        return {
            "name" => @name.getText(),
            "args" => getArgsJSON()
        }
    end

    def getArgsJSON()
        argsJSON = Array.new()
        for arg in @args
            argsJSON.append(arg.toJSON())
        end
        return argsJSON
    end

    def _printLiteral(l)
        l.append("fn:" + @name.getText())
        for arg in @args
            arg._printLiteral(l)
        end
    end

    def _printTokType(type_list)
        type_list.append(@name.getType())
        type_list.append(' ')
        for arg in @args
            type_list.append('|')
            arg._printTokType(type_list)
            
            type_list.append(' ')
        end

    end
end
