require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'
require_relative '../../ASTComponents/InternalStatementComponents/continue_statement.rb'

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
