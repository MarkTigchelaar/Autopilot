require './tokentype.rb'
require_relative './parserutilities.rb'
require_relative './expparser.rb'
require_relative './modparser.rb'
require_relative './importparser.rb'
require_relative '../keywords.rb'
require_relative '../Tokenization/scanner.rb'

class Parser
    def initialize
        @expparser = ExpressionParser.new
        @ExternalStatements = Hash.new
        @LocalStatements = Hash.new
        @tokenizer = Scanner.new
        @ast = nil
        @errorList = Array.new
        @shouldSync = false
        register()
    end

    def parse(filename)
        @tokenizer.loadSource(filename)
        @ast = _parse()
        @tokenizer.closeSource()
    end

    def _parse
        ast = Array.new
        while(@tokenizer.hasTokens() and noErrors()) # remove this later to allow for sync
            ast.append(declaration())
        end
        if(errors())
            return nil
        end
        return ast
    end

    def declaration
        if(match(MODULE))
            return @ExternalStatements[MODULE].parse(self)
        elsif(match(ENUM))
            return nil
        elsif(match(IMPORT))
            return nil
        elsif(match(USE))
            return nil
        elsif(match(STRUCT))
            return nil
        elsif(match(RENAME))
            return nil
        elsif(match(PUB))
            return nil
        elsif(match(FUN))
            return nil
        elsif(match(ACYCLIC))
            return nil
        elsif(match(TRAIT))
            return nil
        elsif(match(UNITTEST))
            return nil
        elsif(match(LIBRARY))
            return nil
        else
            # some error stuff
            return nil
        end
        if(@shouldSync)
            synchronize(self)
            return nil
        end
    end

    def noErrors
        return !errors()
    end

    def errors
        return @errorList.length > 0
    end

    def setToSync
        @shouldSync = true
    end

    def peek
        return @tokenizer.peek()
    end

    def nextToken
        return @tokenizer.nextToken()
    end

    def match(tokenType)
        if(isAtEnd())
            return false
        end
        if(peek().getType() == tokenType)
            return true
        end
        return false
    end

    def discard
        @tokenizer.nextToken()
    end

    def addError(token, message)
        err = Hash.new()
        err["file"] = token.getFilename()
        err["tokenLiteral"] = token.getText()
        err["lineNumber"] = token.getLine()
        err["message"] = message
        @errorList.append(err)
    end

    def register
        @ExternalStatements[MODULE] = ModuleParser.new
        @ExternalStatements[IMPORT] = ImportParser.new
        #@ExternalStatements[CLASS] = ClassStatement.new


    end
end
