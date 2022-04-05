require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'


class WhileParser
    def initialize(expression_parser, statement_parser)
        @expression_parser = expression_parser
        @statement_parser = statement_parser
        @expression_ast = nil
        @statements = Array.new
    end

    def parse(parser)
        reset()
        token = parser.nextToken()
        enforceWhile(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            parseExpression(parser)
        else
            unexpectedToken(parser)
        end
        w = WhileStatement.new(@expression_ast, @statements)
        reset()
        return w
    end

    def parseExpression(parser)
        @expression_parser.loadTokenizer(parser)
        @expression_ast = @expression_parser.parse_expression()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == DO)
            doStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def doStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        else
            parseStatements(parser)
        end
    end

    def parseStatements(parser)
        peekTok = parser.peek()
        while(!isEOF(peekTok) and (is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            stmt = @statement_parser.parse(parser)
            @statements.append(stmt)
            peekTok = parser.peek()
            if(parser.hasErrors())
                return
            end
        end
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            endStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def endStep(parser)
        parser.discard()
    end
    
    def reset()
        @expression_ast = nil
        @statements = Array.new
    end

    def enforceWhile(token)
        if(token.getType() != WHILE)
            throw Exception.new("Did not enounter \"while\" keyword in file " + token.getFilename())
        end
    end
end

class WhileStatement
    def initialize(expression_ast, statements)
        @expression_ast = expression_ast
        @statements = statements
    end

    def _printTokType(type_list)
        if(@expression_ast != nil)
            @expression_ast._printTokType(type_list)
        end
        for stmt in @statements
            stmt._printTokType(type_list)
        end

    end

    def _printLiteral()
        l = Array.new
        @expression_ast._printLiteral(l)
        msg = "exp: " + l.join("")
        #msg += ", statements: "
        #for stmt in @statements
        #    msg += stmt._printLiteral() + ' '
        #end
        return msg
    end
end