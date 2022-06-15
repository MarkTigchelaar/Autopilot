require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'
require_relative './ifparser.rb'

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


class ElifStatement
    def initialize(if_statement)
        @if_statement = if_statement
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        json = @if_statement.toJSON()
        json["type"] = "elif"
        return json
    end

    def _printLiteral
        if(@if_statement != nil)
            return @if_statement._printLiteral()
        end
        return ""
    end

    def _printTokType(type_list)
        if(@if_statement != nil)
            @if_statement._printTokType(type_list)
        end
    end
end