require 'json'
require './Tokenization/scanner.rb'
require './Parsing/expparser.rb'
#require './Parsing/parser.rb'
require './Parsing/modparser.rb'
require './Parsing/importparser.rb'
require './Parsing/defineparser.rb'
require './Parsing/enumparser.rb'
require './Parsing/errorparser.rb'
require './Parsing/unionparser.rb'
require './Parsing/unittestparser.rb'
require './Parsing/functionparser.rb'
require './Parsing/interfaceparser.rb'
require './Parsing/structparser.rb'
#require_relative './keywords.rb'



require './TestingComponents/testingutilities.rb'
require './TestingComponents/DummyParser.rb'
require './TestingComponents/DummyStatementParser.rb'
require './TestingComponents/scannertests.rb'

#require './TestingComponents/generic_parser_tests.rb'

TESTMANIFEST = "../TestFiles/test_manifest.json"

def main

    failurelog = File.open("./failed_tests.txt", 'w')
    jsonfile = File.open(TESTMANIFEST)
    json = JSON.parse(jsonfile.read())
    jsonfile.close()
    tracker = ProgressTracker.new()

    for test in json
        tests = get_tests_from_file(test["test_manifest_file"])
        case test['general_component']
        when "scanner"
            next
            tests.each do |test_case|
                call_scanner_tests(test_case, failurelog, tracker)
            end
        when "expparser"
            next
            tests.each do |test_case|
                call_expparser_tests(test_case, failurelog, tracker)
            end
        when "moduleparser"
            next
            tests.each do |test_case|
                call_moduleparser_tests(test_case, failurelog, tracker)
            end
        when "importparser"
            next
            tests.each do |test_case|
                call_importparser_tests(test_case, failurelog, tracker)
            end
        when "defineparser"
            next
            tests.each do |test_case|
                call_defineparser_tests(test_case, failurelog, tracker)
            end
        when "enumparser"
            next
            tests.each do |test_case|
                call_enumparser_tests(test_case, failurelog, tracker)
            end
        when "errorparser"
            tests.each do |test_case|
                call_errorparser_tests(test_case, failurelog, tracker)
            end
        when "unionparser"
            tests.each do |test_case|
                call_unionparser_tests(test_case, failurelog, tracker)
            end

        when "unittestparser"
            tests.each do |test_case|
                call_unittestparser_tests(test_case, failurelog, tracker)
            end
        when "functionparser"
            tests.each do |test_case|
                call_functionparser_tests(test_case, failurelog, tracker)
            end
        when "interfaceparser"
            tests.each do |test_case|
                call_interfaceparser_tests(test_case, failurelog, tracker)
            end
        when "structparser"
            tests.each do |test_case|
                call_structparser_tests(test_case, failurelog, tracker)
            end
        else
            puts "component #{general_component} not recognized"
            return
        end
    end
    failurelog.close()
    puts tracker.getResults()
    if(tracker.noFailures())
        File.delete("./failed_tests.txt")
    end
end


class ProgressTracker
    def initialize
        @total = 0
        @passed = 0
        @failed = 0
    end

    def incSuccess
        @total += 1
        @passed += 1
    end

    def incFail
        @total += 1
        @failed += 1
    end

    def getResults
        return "Tests passed: #{@passed}/#{@total}, tests failed: #{@failed}/#{@total}"
    end

    def noFailures
        return @failed == 0
    end

end


def call_scanner_tests(test, failurelog, tracker)
    scanner = Scanner.new()
    puts "Testing Scanner, file #{test_case["file"]} ..."
    scanner_tests(scanner, test, failurelog, tracker)
    puts "Done test for Scanner\n"
end


def call_expparser_tests(test_case, failurelog, tracker)
    puts "Testing expression parser, file #{test_case["file"]} ..."
    filename = test_case["file"]
    tokenizer = Scanner.new()
    expParser = ExpressionParser.new()
    expParser.loadTokenizer(tokenizer)
    expParser.loadFile(filename)
    expParser.parseFile()

    generic_parser_tests(expParser, test_case, failurelog, tracker)
    puts "Done test for expression parser\n"
end


def call_moduleparser_tests(test_case, failurelog, tracker)
    dummy = DummyParser.new(ModuleParser.new)
    puts "\nTesting module parser, file #{test_case["file"]} ... "
    dummy.parse(test_case["file"])
    generic_parser_tests(dummy, test_case, failurelog, tracker)
    puts "Done test for module parser"
end


def call_importparser_tests(test_case, failurelog, tracker)
    dummy = DummyParser.new(ImportParser.new)
    puts "\nTesting import parser, file #{test_case["file"]} ... "
    dummy.parse(test_case["file"])
    generic_parser_tests(dummy, test_case, failurelog, tracker)
    puts "Done test for import parser"
end

def call_defineparser_tests(test_case, failurelog, tracker)
    dummy = DummyParser.new(DefineParser.new)
    puts "\nTesting define parser, file #{test_case["file"]} ... "
    dummy.parse(test_case["file"])
    generic_parser_tests(dummy, test_case, failurelog, tracker)
    puts "Done test for define parser"
end

def call_enumparser_tests(test_case, failurelog, tracker)
    dummy = DummyParser.new(EnumParser.new)
    puts "\nTesting enum parser, file #{test_case["file"]} ... "
    dummy.parse(test_case["file"])
    generic_parser_tests(dummy, test_case, failurelog, tracker)
    puts "Done test for enum parser"
end

def call_errorparser_tests(test_case, failurelog, tracker)
    dummy = DummyParser.new(ErrorParser.new)
    puts "\nTesting error parser, file #{test_case["file"]} ... "
    dummy.parse(test_case["file"])
    generic_parser_tests(dummy, test_case, failurelog, tracker)
    puts "Done test for error parser"
end

def call_unionparser_tests(test_case, failurelog, tracker)
    dummy = DummyParser.new(UnionParser.new)
    puts "\nTesting union parser, file #{test_case["file"]} ... "
    dummy.parse(test_case["file"])
    generic_parser_tests(dummy, test_case, failurelog, tracker)
    puts "Done test for union parser"
end

def call_unittestparser_tests(test_case, failurelog, tracker)
    dummy = DummyParser.new(UnittestParser.new(DummyStatementParser.new()))
    puts "\nTesting unit test parser, file #{test_case["file"]} ... "
    dummy.parse(test_case["file"])
    generic_parser_tests(dummy, test_case, failurelog, tracker)
    puts "Done test for unit test parser"
end

def call_functionparser_tests(test_case, failurelog, tracker)
    dummy = DummyParser.new(FunctionParser.new(DummyStatementParser.new()))
    puts "\nTesting function parser, file #{test_case["file"]} ... "
    dummy.parse(test_case["file"])
    generic_parser_tests(dummy, test_case, failurelog, tracker)
    puts "Done test for function parser"
end

def call_interfaceparser_tests(test_case, failurelog, tracker)
    dummy = DummyParser.new(InterfaceParser.new(FunctionParser.new(DummyStatementParser.new())))
    puts "\nTesting interface parser, file #{test_case["file"]} ... "
    dummy.parse(test_case["file"])
    generic_parser_tests(dummy, test_case, failurelog, tracker)
    puts "Done test for interface parser"
end

def call_structparser_tests(test_case, failurelog, tracker)
    dummy = DummyParser.new(StructParser.new(FunctionParser.new(DummyStatementParser.new())))
    puts "\nTesting struct parser, file #{test_case["file"]} ... "
    dummy.parse(test_case["file"])
    generic_parser_tests(dummy, test_case, failurelog, tracker)
    puts "Done test for struct parser"
end

main