require_relative './parserutilities.rb'
require_relative '../tokentype.rb'

class ModuleParser

    def parse(parser)
        peekTok = parser.peek()
        if(peekTok.getText().upcase != MODULE)
            puts "#{MODULE}  #{peekTok.getText()}"
            throw Exception.new("Module parser did not enounter \"module\" keyword in file " + peekTok.getFilename())
        end
        parser.discard()
        msg = "Module names cannot start with numbers, or have non alphanumeric characters."
        if(!isAlphaNumericWord(parser.peek()))
            addError(parser, msg)
            puts "ADDING ERROR"
            return nil
        end
        return ModuleStatement.new(parser.nextToken())
    end
end

class ModuleStatement
    def initialize(moduleinfo)
        @moduleinfo = moduleinfo
    end

    def _printLiteral
        return @moduleinfo.getText()
    end

    def _printTokType(item_list)
        item_list.append(@moduleinfo.getType())
    end
end