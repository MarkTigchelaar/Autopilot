require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'
require_relative './ifparser.rb'
require_relative '../../ASTComponents/InternalStatementComponents/unless_statement.rb'

class UnlessParser
    def initialize(if_parser)
        @if_parser = if_parser
    end

    def parse(parser)
        token = parser.peek()#nextToken()
        enforceUnless(token)
        token.set(IF, "if", "if", token.getLine(), token.getFilename())

        @if_parser.is_unless()
        if_stmt = @if_parser.parse(parser)
        stmt =  UnlessStatement.new(if_stmt)
        @if_parser.isnt_unless()
        return stmt
    end

    def enforceUnless(token)
        if(token.getText().upcase != UNLESS)
            throw Exception.new("Did not enounter \"unless\" keyword in file " + token.getFilename())
        end
    end
end
