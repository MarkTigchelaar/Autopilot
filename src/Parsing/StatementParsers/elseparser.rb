require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

class ElseParser
    def initialize(statement_parser)
        @statement_parser = statement_parser
        @statements = Array.new
    end

    def parse(parser)
        errCount = parser.errorCount()
        reset()
        token = parser.nextToken()
        enforceElse(token)
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        else
            parseStatements(parser)
        end
        e = ElseStatement.new(
            @statements
        )
        reset()
        if(errCount < parser.errorCount())
            internalSynchronize(parser)
        end
        return e
    end

    def parseStatements(parser)
        peekTok = parser.peek()
        if(!isEOF(peekTok) and (is_interal_statement_keyword(peekTok) or isValidIdentifier(peekTok)))
            stmts = @statement_parser.parse(parser)
            @statements = stmts
            peekTok = parser.peek()
        end
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == ENDSCOPE)
            if(@statements.length() == 0)
                emptyStatement(parser)
            else
                endStep(parser)
            end
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

    def enforceElse(token)
        if(token.getText().upcase != ELSE)
            throw Exception.new("Did not enounter \"else\" keyword in file " + token.getFilename())
        end
    end

end

class ElseStatement
    def initialize(sub_statements)
        @sub_statements = sub_statements
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def _printLiteral
        return "else"
    end

    def _printTokType(type_list)
        type_list.append("ELSE")
    end

    def toJSON()
        #stmtsJSON = Array.new()
        #for stmt in @sub_statements
        #    stmtsJSON.append(stmt.toJSON())
        #end

        return {
            "type" => "else",
            "statememts" => @sub_statements.toJSON()
        }
    end
end