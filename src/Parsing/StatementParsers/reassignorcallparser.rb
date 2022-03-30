require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'


class ReassignOrCallParser
    def initialize(expression_parser)
        @expression_parser = expression_parser
        @var_name = nil
        @expression_ast = nil
        @functions = Array.new
    end

    def parse(parser)
        reset()
        name = parser.nextToken()
        enforceIdentifier(name)

        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == EQUAL)
            @var_name = name
            equalStep(parser)
        elsif(peekTok.getType() == LEFT_PAREN)
            callFuncStep(parser, name)
        elsif(peekTok.getType() == DOT)
            @var_name = name
            dotStep(parser)
        else
            unexpectedToken(parser)
        end
        r = ReassignmentOrCallStatement.new(@name, @expression_ast, @functions)
        reset()
        return r
    end

    def equalStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        else
            parseExpression(parser)
        end
    end

    def parseExpression(parser)
        @expression_parser.loadTokenizer(parser)
        @expression_ast = @expression_parser.parse_expression()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(!is_interal_statement_keyword(peekTok) and !isValidIdentifier(peekTok))
            unexpectedToken(parser)
        end
    end

    def callFuncStep(parser, name)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(!isValidIdentifier(peekTok))
            unexpectedToken(parser)
        end
        args = Array.new
        @expression_parser.loadTokenizer(parser)
        while(!isEOF(peekTok))
            args.append(@expression_parser.parse_expression())
            peekTok = parser.peek()
            if(isEOF(peekTok))
                eofReached(parser)
            elsif(peekTok.getType() == COMMA)
                parser.discard()
                peekTok = parser.peek()
            elsif(peekTok.getType() == RIGHT_PAREN)
                break
            else
                unexpectedToken(parser)
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
        if(isEOF(peekTok))
            eofReached(parser)
        else
            parseExpression(parser)
        end
    end

    def reset
        @var_name = nil
        @expression_ast = nil
        @functions = Array.new
    end

    def enforceIdentifier(token)
        if(!isValidIdentifier(token))
            throw Exception.new("Did not enounter \"valid identifier\" in file " + token.getFilename())
        end
    end
end

class FuncCall
    def initialize(name, args)
        @name = name
        @args = args
    end
end

class ReassignmentOrCallStatement
    def initialize(var_name, expression_ast, functions)
        @var_name = var_name
        @expression_ast = expression_ast
        @functions = functions
    end
end