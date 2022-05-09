require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

class ContinueParser
    def parse(parser)
        token = parser.nextToken()
        enforceContinue(token)
        return ContinueStatement.new(token)
    end

    def enforceContinue(token)
        if(token.getText().upcase != CONTINUE)
            throw Exception.new("Did not enounter \"contiue\" keyword in file " + token.getFilename())
        end
    end
end

class ContinueStatement
    def initialize(token)
        @information = token
    end

    def _printLiteral
        return @information.getText()
    end

    def _printTokType(type_list)
        type_list.append(@information.getType())
    end

    def toJSON()
        return {
            "type" => "continue",
            "line_number" => @information.getLine()
        }
    end
end