require './Tokenization/scanner.rb'
require './Parsing/expression_parser.rb'

require './Parsing/ExternalStatementParsers/modparser.rb'
require './Parsing/ExternalStatementParsers/importparser.rb'
require './Parsing/ExternalStatementParsers/defineparser.rb'
require './Parsing/ExternalStatementParsers/enumparser.rb'
require './Parsing/ExternalStatementParsers/errorparser.rb'
require './Parsing/ExternalStatementParsers/unionparser.rb'
require './Parsing/ExternalStatementParsers/unittestparser.rb'
require './Parsing/ExternalStatementParsers/functionparser.rb'
require './Parsing/ExternalStatementParsers/interfaceparser.rb'
require './Parsing/ExternalStatementParsers/structparser.rb'

require './Parsing/InternalStatementParsers/returnparser.rb'
require './Parsing/InternalStatementParsers/continueparser.rb'
require './Parsing/InternalStatementParsers/breakparser.rb'
require './Parsing/InternalStatementParsers/loopparser.rb'
require './Parsing/InternalStatementParsers/switchparser.rb'
require './Parsing/InternalStatementParsers/ifparser.rb'
require './Parsing/InternalStatementParsers/elseparser.rb'
require './Parsing/InternalStatementParsers/elifparser.rb'
require './Parsing/InternalStatementParsers/unlessparser.rb'
require './Parsing/InternalStatementParsers/assignparser.rb'
require './Parsing/InternalStatementParsers/whileparser.rb'
require './Parsing/InternalStatementParsers/forparser.rb'
require './Parsing/InternalStatementParsers/reassignorcallparser.rb'
require './Parsing/InternalStatementParsers/statementparser.rb'
require './Parsing/parser.rb'

require './TestingComponents/testingutilities.rb'
require './TestingComponents/DummyParser.rb'
require './TestingComponents/DummyStatementParser.rb'
require './TestingComponents/scannertests.rb'



def phase_one_tests(failurelog, tracker, json)
    tokenizer = Scanner.new()

    for test in json
        tokenizer.reset()
        tests = get_tests_from_file(test["test_manifest_file"])
        general_component = test['general_component']
        case general_component
        when "scanner"
            #next
            tests.each do |test_case|
                call_scanner_tests(test_case, failurelog, tracker)
                
            end
        when "expparser"
            #next
            name = "expression"
            expparser = ExpressionParser.new()
            expparser.loadTokenizer(Scanner.new())
            tests.each do |test_case|
                call_expparser_tests(test_case, failurelog, tracker, expparser)
            end
        when "moduleparser"
            #next
            m = ModuleParser.new
            tests.each do |test_case|
                d = DummyParser.new(m, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "module")
            end
        when "importparser"
            #next
            i = ImportParser.new
            tests.each do |test_case|
                d = DummyParser.new(i, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "import")
            end
        when "defineparser"
            #next
            de = DefineParser.new
            tests.each do |test_case|
                d = DummyParser.new(de, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "define")
            end
        when "enumparser"
            #next
            e = EnumParser.new
            tests.each do |test_case|
                d = DummyParser.new(e, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "enum")
            end
        when "errorparser"
            #next
            e = ErrorParser.new
            tests.each do |test_case|
                d = DummyParser.new(e, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "error")
            end
        when "unionparser"
            #next
            u = UnionParser.new
            tests.each do |test_case|
                d = DummyParser.new(u, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "union")
            end

        when "unittestparser"
            #next
            u = UnittestParser.new(DummyStatementParser.new())
            tests.each do |test_case|
                d = DummyParser.new(u, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "unit test")
            end
        when "functionparser"
            #next
            f = FunctionParser.new(DummyStatementParser.new())
            tests.each do |test_case|
                d = DummyParser.new(f, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "function")
            end
        when "interfaceparser"
            #next
            i = InterfaceParser.new(FunctionParser.new(DummyStatementParser.new()))
            tests.each do |test_case|
                d = DummyParser.new(i, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "interface")
            end
        when "structparser"
            #next
            s = StructParser.new(FunctionParser.new(StatementParser.new(ExpressionParser.new)))
            tests.each do |test_case|
                d = DummyParser.new(s, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "struct")
            end
        when "returnparser"
            #next
            expParser = ExpressionParser.new()
            expParser.loadTokenizer(tokenizer)
            r = ReturnParser.new(expParser)
            tests.each do |test_case|
                d = DummyParser.new(r, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "return")
            end
        when "continueparser"
            #next
            c = ContinueParser.new
            tests.each do |test_case|
                d = DummyParser.new(c, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "continue")
            end
        when "breakparser"
            #next
            b = BreakParser.new
            tests.each do |test_case|
                d = DummyParser.new(b, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "break")
            end
        when "loopparser"
            #next
            l = LoopParser.new(DummyStatementParser.new)
            tests.each do |test_case|
                d = DummyParser.new(l, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "loop")
            end
        when "switchparser"
            #next
            s = SwitchParser.new(DummyStatementParser.new)
            tests.each do |test_case|
                d = DummyParser.new(s, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "switch")
            end
        when "ifparser"
            #next
            i = IfParser.new(ExpressionParser.new, DummyStatementParser.new)
            tests.each do |test_case|
                d = DummyParser.new(i, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "if")
            end
        when "elseparser"
            #next
            ep = ExpressionParser.new
            sp = DummyStatementParser.new
            ip = IfParser.new(ep, sp)
            i = ElseParser.new(sp)
            tests.each do |test_case|
                d = DummyParser.new(i, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "else")
            end
        when "unlessparser"
            #next
            ep = ExpressionParser.new
            sp = DummyStatementParser.new
            ip = IfParser.new(ep, sp)
            u = UnlessParser.new(ip)
            tests.each do |test_case|
                d = DummyParser.new(u, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "unless")
            end
        when "elifparser"
            #next
            ep = ExpressionParser.new
            sp = DummyStatementParser.new
            ip = IfParser.new(ep, sp)
            e = ElifParser.new(ip)
            tests.each do |test_case|
                d = DummyParser.new(e, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "elif")
            end
        when "assignparser"
            #next
            a = AssignParser.new(ExpressionParser.new)
            tests.each do |test_case|
                d = DummyParser.new(a, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "assign")
            end
        when "whileparser"
            #next
            w = WhileParser.new(ExpressionParser.new, DummyStatementParser.new)
            tests.each do |test_case|
                d = DummyParser.new(w, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "while")
            end
        when "forparser"
            #next
            f = ForParser.new(ExpressionParser.new, DummyStatementParser.new)
            tests.each do |test_case|
                d = DummyParser.new(f, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "for")
            end
        when "reassignorcallparser"
            #next
            r = ReassignOrCallParser.new(ExpressionParser.new)
            tests.each do |test_case|
                d = DummyParser.new(r, tokenizer)
                call_parser_component_tests(test_case, failurelog, tracker, d, "reassign or call")
            end
        when "statementparserwdummy"
            #next
            s = StatementParser.new(ExpressionParser.new(), DummyStatementParser.new())
            tests.each do |test_file|
                d = DummyParser.new(s, tokenizer)
                call_statement_component_tests(test_file, failurelog, tracker, d, "statement with dummy")
            end
        when "statementcombinations"
            #next
            s = StatementParser.new(ExpressionParser.new())
            tests.each do |test_file|
                d = DummyParser.new(s, tokenizer)
                call_parser_component_tests(test_file, failurelog, tracker, d, "statement")
            end
        when "statementsequences"
            #next 
            s = StatementParser.new(ExpressionParser.new())
            tests.each do |test_file|
                d = DummyParser.new(s, tokenizer)
                call_parser_component_tests(test_file, failurelog, tracker, d, "statement")
            end
        when "mainparser"
            #next
            parser = Parser.new()
            tests.each do |test_file|
                call_statement_component_tests(test_file, failurelog, tracker, parser, "main", true)
            end
        when "mainparserJSON"
            parser = Parser.new()
            call_toJSONTests(test, failurelog, tracker, parser, "main")
        else
            puts "component #{general_component} not recognized"
            return
        end
    end
end


def call_scanner_tests(test, failurelog, tracker)
    scanner = Scanner.new()
    puts "Testing Scanner, file #{test["file"]} ..."
    scanner_tests(scanner, test, failurelog, tracker)
    puts "Done test for Scanner\n"
end

def call_expparser_tests(test_case, failurelog, tracker, expParser)
    puts "Testing expression parser, file #{test_case["file"]} ..."
    filename = test_case["file"]
    expParser.loadFile(filename)
    expParser.parseFile()

    generic_tests(expParser, test_case, failurelog, tracker)
    puts "Done test for expression parser\n"
end

def call_parser_component_tests(test_case, failurelog, tracker, parser, name)
    puts "\nTesting #{name} parser, file #{test_case["file"]} ... "
    parser.parse(test_case["file"])
    begin
    generic_tests(parser, test_case, failurelog, tracker)
    rescue
        puts "call_parser_component_tests hit a problem"
    end
    puts "Done test for #{name} parser"
end

def call_statement_component_tests(test_file, failurelog, tracker, parser, name, main_parser=false)
    tests = get_tests_from_file(test_file)
    for test_case in tests
        puts "\nTesting #{name} parser, file #{test_case["file"]} ... "
        if(!main_parser)
            parser.parse(test_case["file"], true)
        else
            parser.parse(test_case["file"])
        end
        generic_tests(parser, test_case, failurelog, tracker)
        if(main_parser)
            next
        end
        parser.reset()
    end
    puts "Done test for #{name} parser"
end

def call_toJSONTests(test, failurelog, tracker, parser, name)
    tests = get_tests_from_file(test["test_manifest_file"])
    blow_up = false
    for test_case in tests
        puts "\nTesting #{name} parser, JSON file #{test_case["file"]} ... "
        parser.parse(test_case["file"])
        if(parser.hasErrors())
            puts("Errors found!")
            printErrors(parser.getErrorList())
            blow_up = true
            break
        end
        produced_ast = parser.toJSON()
        compare_asts(produced_ast, test_case["ast"], test_case, failurelog, tracker)
        parser.reset()
    end
    if(blow_up)
        raise Exception.new("Cannot continue, JSON tests are happy path tests, but errors detected.")
    end
    puts "Done test for #{name} parser"
end