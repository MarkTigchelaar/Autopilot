require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'
require_relative './ifparser.rb'
require_relative '../../ASTComponents/InternalStatementComponents/elif_statement.rb'

class ElifParser
    def initialize(if_parser)
        @if_parser = if_parser
    end

    def parse(parser)
        token = parser.peek()
        enforceElif(token)
        token.set(IF, "if", "if", token.getLine(), token.getFilename())
        if_stmt = @if_parser.parse(parser) 
        return ElifStatement.new(if_stmt)
    end

    def enforceElif(token)
        if(token.getText().upcase != ELIF)
            throw Exception.new("Did not enounter \"elif\" keyword in file " + token.getFilename())
        end
    end
end
