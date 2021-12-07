

class Token
    def initialize(tok_type, text, literal, line, filename)
        @tok_type = tok_type
        @text = text
        @literal = literal 
        @line = line 
        @filename = filename
    end

    def print
        return "filename: #{@filename} line: #{(@line).to_s} token type: #{@tok_type} text: #{@text}"
    end

    def getText
        return @text
    end

end