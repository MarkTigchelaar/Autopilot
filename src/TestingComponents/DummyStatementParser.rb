require_relative '../Parsing/parserutilities.rb'

class DummyStatementParser
    def parse(parser)
        current = parser.nextToken()
        if(isEOF(current))
            eofReached(parser)
        elsif(is_interal_statement_keyword(current))
            # actual parser will be able to handle print(), thing.method() etc.
            return DummyStatement.new(current)
        else
            raise Exception.new("Failed to return dummy Statement")
        end
    end
end


class DummyStatement
    def initialize(name, left_stmt, right_stmt)
        @name = name
        @left_stmt = left_stmt
        @right_stmt = right_stmt
    end

    def getType()
        return @name.getType()
    end
end