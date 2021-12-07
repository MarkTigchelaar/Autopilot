require './Tokenization/scanner.rb'
require_relative './keywords.rb'
require 'json'

TESTMANIFEST = "../TestFiles/alltests.json"
SUCCESS = "TEST CASE PASSED"
FAILURE = "TEST CASE FAILED"
def main

    failurelog = File.open("./failed_tests.txt", 'w')
    
    jsonfile = File.open(TESTMANIFEST)
    json = JSON.parse(jsonfile.read())
    jsonfile.close()

    for test in json
        case test['component']
        when "scanner"
            scanner_test(test, failurelog)
        else
            puts "component #{component} not recognized"
            return
        end
        
    end
    failurelog.close()

end


def scanner_test(test, failurelog)
    puts "----- TESTING SCANNER -----"
    testfile = File.open(test['file'])
    scanner = Scanner.new()
    tokens = Array.new()
    contents = testfile.read()
    scanner.loadSource(contents)

    tokens = scanner.scanTokens()
    expected = test['expected']

    for i in 0 .. tokens.length - 1
        #puts tokens[i].class
        if(i == tokens.length - 1 or tokens[i].getText == "EOF")
            next
        end
        if(tokens[i].getText() != expected[i])
            msg = FAILURE + " Scanner failed test, expected \"#{expected[i]}\", got \"#{tokens[i].getText}\""
            puts msg
            failurelog.write("In #{test['file']}" + "\n")
            failurelog.write(msg + "\n\n")
        else
            puts SUCCESS + " Scanner passed test, expected \"#{expected[i]}\", got \"#{tokens[i].getText}\""
        end
    end

    puts "\n"
    
end

main