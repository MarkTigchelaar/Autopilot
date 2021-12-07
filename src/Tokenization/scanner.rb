require_relative '../keywords.rb'
require_relative '../tokentype.rb'
require_relative './token.rb'

class Scanner 
    def initialize()
        @source = nil#_source
        @tokens = Array.new()
        @start = 0
        @current = 0
        @line = 1
        @filename = "testing"
        @keywords = getkeywords()
    end

    def loadSource(_source)
        @source = _source
    end

    def scanTokens
        while(!isAtEnd()) do
            @start = @current
            #puts "start and current are #{@start}"
            scanToken()
        end
        @tokens.append(Token.new(EOF, "", nil, @line, @filename))
        return @tokens
    end

    def scanToken
        char = advance()
        #puts "Scanning character: \"#{char}\""
        
        case char
        when "("
            addToken(LEFT_PAREN)
        when ")"
            addToken(RIGHT_PAREN)
        when ","
            addToken(COMMA)
        when "["
            addToken(LEFT_BRACKET)
        when "]"
            addToken(RIGHT_BRACKET)
        when "{"
            addToken(LEFT_BRACE)
        when "}"
            addToken(RIGHT_BRACE)
        when "?"
            addToken(QUESTION)
        when "."
            if(match("."))
                addToken(RANGE)
            else
                addToken(DOT)
            end
        when "="
            if(match("="))
                addToken(EQUAL_EQUAL)
            else
                addToken(EQUAL)
            end
        when "+"
            if(match("="))
                addToken(PLUS_EQUAL)
            else
                addToken(PLUS)
            end
        when "-"
            if(match("="))
                addToken(MINUS_EQUAL)
            else
                addToken(MINUS)
            end
        when "*"
            if(match("="))
                addToken(STAR_EQUAL)
            else
                addToken(STAR)
            end
        when "/"
            if(match("/"))
                while( peek() != "\n" and not isAtEnd())
                    advance()
                end
            elsif(match("*"))
                multilineComment()
            elsif(match("="))
                addToken(SLASH_EQUAL)
            else
                addToken(SLASH)
            end
        when "^"
            if(match("="))
                addToken(CARROT_EQUAL)
            else
                addToken(CARROT)
            end
        when "%"
            if(match("="))
                addToken(MOD_EQUAL)
            else
                addToken(MOD)
            end
        when "!"
            if(match("="))
                addToken(BANG_EQUAL)
            else
                addToken(BANG)
            end
        when "<"
            if(match("="))
                addToken(LESS_EQUAL)
            else
                addToken(LESS)
            end
        when ">"
            if(match("="))
                #puts "Matched >="
                addToken(GREATER_EQUAL)
            else
                addToken(GREATER)
            end
        when "%"
            if(match("="))
                addToken(MOD_EQUAL)
            else
                addToken(MOD)
            end
        when " ", "\r", "\t"
            nothing = ""
            #puts "found whitespace, skipping"
        when "\""
            string()
        when "\n"
            @line += 1
        else
            if(isDigit(char))
                ##puts "#{char} is a digit"
                number()
            elsif(isAlpha(char))
                #puts "#{char} is alphabetical"
                identifier()
            else
                scanner_error("Unexpected character: #{char}")
            end
        end
        #puts "\n\n\n"
    end

    def identifier()
        #puts "In identifier method"
        while(isAlphaNumeric(peek()))
            #puts "peeked character: #{peek()}"
            advance()
        end
        text = @source[@start .. @current - 1]
        #puts "(in identifier) text: \"#{text}\""
        type = @keywords[text]
        #puts "type: #{type}"
        if(type == nil)
            type = IDENTIFIER
        end
        addToken(type)
    end

    def number
        while(isDigit(peek()))
            advance()
        end
        isfloat = false
        if(peek() == "." and isDigit(peekNext()))
            isfloat = true
            advance()
            while(isDigit(peek()))
                advance()
            end
        end
        if(isfloat)
            addToken(FLOAT)
        else
            addToken(INT)
        end
    end

    def isDigit(char)
        return ((char >= "0") and (char <= "9"))
    end

    def isAlpha(char)
        islowercase = (char.ord >= 'a'.ord && char.ord <= 'z'.ord)
        isuppercase = (char.ord >= 'A'.ord && char.ord <= 'Z'.ord)
        return (islowercase or isuppercase or char == '_')
    end

    def isAlphaNumeric(char)
        #puts "Checking \"#{char}\" in isAlphnumeric"
        return (isAlpha(char) or isDigit(char))
    end

    def scanner_error(message)
        print "ERROR: In #{@filename} at #{(@line).to_s} \"" + message + "\""
    end

    def addToken(tok_type, literal = nil)
        #puts "adding Token"
        s = @start
        f = @current

        ##puts "start: #{s}, current: #{f}"
        ##puts "all: #{@source[0, f]}"
        ##puts "from start: #{@source[s, @source.length]}"

        text = @source[s .. f - 1]
        #puts "text: \"#{text}\""
        ##puts "start: #{s}, current: #{f}\n\n"

        @tokens.append(Token.new(tok_type, text, literal, @line, @filename))
    end

    def advance
        @current += 1
        return @source[@current - 1]
    end

    def isAtEnd
        return @current >= @source.length
    end

    def match(expected)
        if(isAtEnd())
            #puts "In match, reached end"
            return false
        end
        if(@source[@current] != expected)
            #puts "In match expected #{expected}, got #{@source[@current]}"
            return false
        end
        #puts "In match expected #{expected}, did match"
        @current += 1
        return true
    end

    def peek
        if(isAtEnd())
            return "\0"
        end
        return @source[@current]
    end

    def peekNext
        if(@current + 1 >= @source.length)
            return "\0"
        end
        return @source[@current + 1]
    end

    def multilineComment
        comment_sections = 1

        while(not isAtEnd())
            current = peek()

            if(current == "/" and peekNext() == "*")
                comment_sections += 1
            end

            if(current == "*" and peekNext() == "/")
                comment_sections -= 1
            end

            if(current == "\n")
                @line += 1
            end

            advance()

            if(comment_sections == 0)
                advance()
                break
            end
        end

        if(comment_sections > 0)
            print "line #{(line).to_s} Unterminated block comment."
        end
    end

    def string
        while(peek() != "\"" and not isAtEnd())
            if(peek() == "\n")
                @line += 1
            end
            if(peek() == "\\")
                if(peekNext() == "\"")
                    advance()
                end
            end

            advance()
        end

        if(isAtEnd())
            scanner_error("Unterminated string.")
        end

        advance()

        value = @source[@start + 1, @current - 1]
        addToken(STRING, value)
    end

end