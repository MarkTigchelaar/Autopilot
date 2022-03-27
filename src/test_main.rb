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
require './Parsing/StatementParsers/returnparser.rb'
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
    tokenizer = Scanner.new()

    for test in json
        tokenizer.reset()
        tests = get_tests_from_file(test["test_manifest_file"])
        case test['general_component']
        when "scanner"
            next
            tests.each do |test_case|
                call_scanner_tests(test_case, failurelog, tracker)
                
            end
        when "expparser"
            next
            name = "expression"
            expparser = ExpressionParser.new()
            expparser.loadTokenizer(Scanner.new())
            tests.each do |test_case|
                expparser.loadFile(test_case["file"])
                expparser.parseFile()
                #call_expparser_tests(test_case, failurelog, tracker)
                call_parser_component_tests(test_case, failurelog, tracker, expparser, name)
            end
        when "moduleparser"
            m = ModuleParser.new
            tests.each do |test_case|
                d = DummyParser.new(m, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "module")
            end
        when "importparser"
            i = ImportParser.new
            tests.each do |test_case|
                d = DummyParser.new(i, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "import")
            end
        when "defineparser"
            de = DefineParser.new
            tests.each do |test_case|
                d = DummyParser.new(de, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "define")
            end
        when "enumparser"
            e = EnumParser.new
            tests.each do |test_case|
                d = DummyParser.new(e, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "enum")
            end
        when "errorparser"
            e = ErrorParser.new
            tests.each do |test_case|
                d = DummyParser.new(e, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "error")
            end
        when "unionparser"
            u = UnionParser.new
            tests.each do |test_case|
                d = DummyParser.new(u, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "union")
            end

        when "unittestparser"
            u = UnittestParser.new(DummyStatementParser.new())
            tests.each do |test_case|
                d = DummyParser.new(u, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "unit test")
            end
        when "functionparser"
            f = FunctionParser.new(DummyStatementParser.new())
            tests.each do |test_case|
                d = DummyParser.new(f, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "function")
            end
        when "interfaceparser"
            i = InterfaceParser.new(FunctionParser.new(DummyStatementParser.new()))
            tests.each do |test_case|
                d = DummyParser.new(i, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "interface")
            end
        when "structparser"
            s = StructParser.new(FunctionParser.new(DummyStatementParser.new()))
            tests.each do |test_case|
                d = DummyParser.new(s, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "struct")
            end
        when "returnparser"
            tests.each do |test_case|
                call_returnparser_tests(test_case, failurelog, tracker)
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

def call_returnparser_tests(test_case, failurelog, tracker)
    tokenizer = Scanner.new()
    expParser = ExpressionParser.new()
    expParser.loadTokenizer(tokenizer)
    dummy = DummyParser.new(ReturnParser.new(expParser))



    puts "\nTesting return parser, file #{test_case["file"]} ... "
    dummy.parse(test_case["file"])
    generic_parser_tests(dummy, test_case, failurelog, tracker)
    puts "Done test for return parser"
end

def call_parser_component_tests(test_case, failurelog, tracker, parser, name)
    puts "\nTesting #{name} parser, file #{test_case["file"]} ... "
    parser.parse(test_case["file"])
    generic_parser_tests(parser, test_case, failurelog, tracker)
    puts "Done test for #{name} parser"
end

main