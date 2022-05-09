require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'

class BreakParser

    def initialize()
        @loop_label = nil
    end

    def parse(parser)
        @loop_label = nil
        token = parser.nextToken()
        enforceBreak(token)
        peekTok = parser.peek()
        if(peekTok.getType() == LEFT_PAREN)
            leftParenStep(parser)
        end
        b = BreakStatement.new(@loop_label, token)
        @loop_label = nil
        return b
    end

    def leftParenStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            labelNameStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def labelNameStep(parser)
        @loop_label = parser.nextToken()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == RIGHT_PAREN)
            rightParenStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def rightParenStep(parser)
        parser.discard()
    end

    def enforceBreak(token)
        if(token.getText().upcase != BREAK)
            throw Exception.new("Did not enounter \"break\" keyword in file " + token.getFilename())
        end
    end
end

class BreakStatement
    def initialize(loop_label, token)
        @loop_label = loop_label
        @information = token
    end

    def _printLiteral
        if(@loop_label != nil)
            return @loop_label.getText() + ", " + @information.getText()
        end
        return @information.getText()
    end

    def _printTokType(type_list)
        if(@loop_label != nil)
            type_list.append(@loop_label.getType())
        end
        type_list.append(@information.getType())
    end

    def toJSON()
        return {
            "type" => "break",
            "loop_label" => {
                "literal" => @information.getText(),
                "type" => @information.getType(),
                "line_number" => @information.getLine()
            }
        }
    end
end