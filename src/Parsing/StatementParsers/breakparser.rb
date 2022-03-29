require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

class BreakParser
    def parse(parser)
        token = parser.nextToken()
        enforceBreak(token)
        return BreakStatement.new(token)
    end

    def enforceBreak(token)
        if(token.getText().upcase != BREAK)
            throw Exception.new("Did not enounter \"break\" keyword in file " + token.getFilename())
        end
    end
end

class BreakStatement
    def initialize(token)
        @information = token
    end

    def _printLiteral
        return @information.getText()
    end
end