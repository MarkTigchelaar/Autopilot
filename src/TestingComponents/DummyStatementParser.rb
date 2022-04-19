require_relative '../Parsing/parserutilities.rb'

class DummyStatementParser
    def parse(parser)
        current = parser.nextToken()
        if(isEOF(current))
            eofReached(parser)
        elsif(is_interal_statement_keyword(current))
            # actual parser will be able to handle print(), thing.method() etc.
            d = DummyStatement.new(current)
            a = Array.new
            a.append(d)
            return a
        else
            raise Exception.new("Failed to return dummy Statement")
        end
    end
end


class DummyStatement
    def initialize(name, left_stmt = nil, right_stmt = nil)
        @name = name
        @left_stmt = left_stmt
        @right_stmt = right_stmt
    end

    def getType()
        return @name.getType()
    end

    def _printLiteral
        return @name.getText()
    end

    def _printTokType(type_list)
        type_list.append(@name.getType())
    end
end