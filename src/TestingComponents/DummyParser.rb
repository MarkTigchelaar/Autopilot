require_relative '../Tokenization/scanner.rb'

class DummyParser
    def initialize(testComponent, tokenizer = nil)
        @scanner = tokenizer || Scanner.new()
        @err = nil
        @component = testComponent
        @ast = nil
    end

    def addError(token, msg)
        @err = Hash.new
        @err["file"] = token.getFilename()
        @err["tokenLiteral"] = token.getText()
        @err["lineNumber"] = token.getLine()
        @err["message"] = msg
    end

    def hasErrors
        return @err != nil
    end

    def getErrorList
        errors = Array.new()
        if @err != nil
            errors.append(@err)
        end
        return errors
    end

    def parse(filename)
        @scanner.loadSource(filename)
        @ast = @component.parse(self)
        @scanner.closeSource()
    end

    def astString
        return @ast._printLiteral()
    end

    def tokenTypeString
        type_list = Array.new()
        #type_list.append("(")
        #type_list = @ast._printTokType(type_list)
        #type_list.append(")")
        concact_all_strings = ""
        return ""#type_list.join(concact_all_strings)
    end

    def peek
        return @scanner.peekToken()
    end

    def nextToken
        return @scanner.nextToken()
    end

    def setToSync
        return
    end

    def discard
        nextToken()
    end
end