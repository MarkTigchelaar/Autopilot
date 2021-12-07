require './Tokenization/scanner.rb'
require './keywords.rb'

def main
    if ARGV.length < 1
        useage()
        return
    end
    scanner = Scanner.new()
    tokens = Array.new()
    filetokens = Array.new()
    for arg in ARGV
        puts arg
        
        if arg.end_with?("ap")
            file = File.open(arg)
            contents = file.read()
            scanner.loadSource(contents)
            filetokens = scanner.scanTokens()
            for tok in filetokens
                tokens.append(tok)
            end
        end
    end
    
    
    for tok in tokens
        puts tok.print() + "\n"
    end
end

def useage()
    "put useage stuff here"
end








main