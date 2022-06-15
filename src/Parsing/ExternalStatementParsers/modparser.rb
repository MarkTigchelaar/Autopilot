require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'

class ModuleParser

    def parse(parser)
        peekTok = parser.peek()
        if(peekTok.getText().upcase != MODULE)
            throw Exception.new("Module parser did not enounter \"module\" keyword in file " + peekTok.getFilename())
        end
        parser.discard()
        msg = "Module names cannot start with numbers, or have non alphanumeric characters."
        if(!isAlphaNumericWord(parser.peek()))
            ERRORS::addError(parser, msg)
            return nil
        end
        return ModuleStatement.new(parser.nextToken())
    end
end

class ModuleStatement
    def initialize(moduleinfo)
        @moduleinfo = moduleinfo
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node(self)
    end

    def toJSON()
        return {
            "type" => "module",
            "name" => {
                "literal" => @moduleinfo.getText(),
                "type" => @moduleinfo.getType(),
                "line_number" => @moduleinfo.getLine()
            }
        }
    end

    def _printLiteral
        return @moduleinfo.getText()
    end

    def _printTokType(item_list)
        item_list.append(@moduleinfo.getType())
    end
end
