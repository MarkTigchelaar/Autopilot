require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../ASTComponents/ExternalStatementComponents/module_statement.rb'

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
