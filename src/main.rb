require_relative './Parsing/parser.rb'
require './TestingComponents/testingutilities.rb'
require 'json'


def main
    if ARGV.length < 1
        useage()
        return
    end
    parser = Parser.new()

    astList = Array.new()
    for arg in ARGV
        if arg.end_with?("ap")
            parser.parse(arg)
            if(parser.hasErrors())
                break
            end
            astList.append(parser.toJSON())
        end
    end
    if(parser.hasErrors())
        puts("Errors found!")
        printErrors(parser.getErrorList())
    end

    astStrings = Array.new()
    for ast in astList
        jsonString = JSON.dump(ast)
        astStrings.append(jsonString)
        puts jsonString
    end
end

def useage()
    puts "put useage stuff here"
end








main