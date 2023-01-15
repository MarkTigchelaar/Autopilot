require_relative '../Tokenization/scanner.rb'
require 'set.rb'
class DummyParser
    def initialize(testComponent, tokenizer = nil)
        @scanner = tokenizer || Scanner.new()
        @err = Array.new
        @component = testComponent
        @ast = nil
    end

    def addError(token, msg)
        err = Hash.new
        err["file"] = token.getFilename()
        err["tokenLiteral"] = token.getText()
        err["lineNumber"] = token.getLine()
        err["message"] = msg
        @err.append(err)
    end

    def hasErrors
        return (@err != nil and @err.length > 0)
    end

    def errorCount()
        return @err.length()
    end

    def getErrorList

        dup_indicies = Set.new
        for i in (@err.length - 1).downto(0) do
            for j in (i - 1).downto(0) do
                if(i == j)
                    next
                end
                b = @err[j]
                same_file = @err[i]["file"] == b["file"]
                same_lit = @err[i]["tokenLiteral"] == b["tokenLiteral"]
                same_line = @err[i]["lineNumber"] == b["lineNumber"]
                same_msg = @err[i]["message"] == b["message"]
                is_eof = b["message"] == "End of file reached."
                if(same_file and same_lit and same_line and same_msg and is_eof)
                    dup_indicies.add(i)
                end
            end
        end
        for i in (@err.length - 1).downto(0) do
            if dup_indicies.include?(i)
                @err.delete_at(i)
            end
        end

        return @err
    end

    def reset()
        @ast = nil
        @err = Array.new
    end

    def parse(filename, component_test = false)
        reset()
        @scanner.loadSource(filename)
        if(component_test)
            @ast = @component.parse(self, true)
        else
            @ast = @component.parse(self)
        end
        @scanner.closeSource()
    end

    def astString
        return @ast._printLiteral()
    end

    def tokenTypeString
        type_list = Array.new()
        @ast._printTokType(type_list)
        concact_all_strings = " "
        str = type_list.join(concact_all_strings)
        str = str.strip()
        str = str.squeeze(" ")
        return str
    end

    def peekToken()
        peek()
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

    def canDiscardEndTok()
        return @scanner.bytesFromEnd() > 3
    end

    def discard
        nextToken()
    end
end