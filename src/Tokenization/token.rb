
# literal and text are the same thing, replace "text" with "literal" in entire code
class Token
    def initialize(tok_type, text, literal, line, filename)
        @tok_type = tok_type
        @text = text
        @literal = text 
        @line = line 
        @filename = filename
    end

    def print
        return "\n filename: #{@filename}\n line: #{(@line).to_s}\n token type: #{@tok_type}\n literal: #{@literal}\n\n\n"
    end

    def getText
        return @literal
    end

    def getFilename
        return @filename
    end

    def getLine
        return @line.to_s()
    end

    def getType
        return @tok_type
    end

end